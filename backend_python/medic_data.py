from __main__ import app, stderr, request, mysql, validate_json, format_sql, make_response, json,\
time, datetime

def get_login_id(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID FROM LOGIN_DETAILS WHERE USERNAME = '{}'"
                    .format(username))
    login_id = -1
    response_db = cur.fetchone()
    if response_db is not None and response_db[0] is not None:
        login_id = int(response_db[0])
    return login_id

@app.route("/medic_list", methods = ["GET", "POST", "DELETE"])
def medic_details():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM MEDIC_DETAILS")
        response_db = cur.fetchall()
        if response_db is not None:
            list_of_medics = []
            for entry in response_db:
                list_of_medics.append({"sname": entry[1], "lname": entry[2],
                                    "rating": float(entry[3])})
            cur.close()
            return make_response(json.dumps(list_of_medics), 200)
        cur.close()
        return make_response({"message": "No medics found"}, 400)
    elif request.method == "POST":
        data_received = request.get_json()
        if not validate_json(["username", "sname", "lname", "rating"], data_received):
            cur.close()
            return make_response({"message": "Invalid json"}, 400)
        if float(data_received["rating"]) > 5 or float(data_received["rating"] < 0):
            cur.close()
            return make_response({"message": "Bad rating"}, 400)
        cur.execute("SELECT ID FROM LOGIN_DETAILS WHERE USERNAME = '{}'"
                    .format(data_received["username"]))
        medic_id = get_login_id(data_received["username"])
        if medic_id == -1:
            return make_response({"message": "Bad username"}, 400)
        query = """
        INSERT INTO MEDIC_DETAILS (ID, SNAME,
                                    LNAME,
                                    RATING)
            VALUES ({medic_id}, {sname},
                    {lname}, {rating});
        """.format(
            medic_id    = medic_id,
            sname       = format_sql(data_received["sname"]),
            lname       = format_sql(data_received["lname"]),
            rating      = data_received["rating"]
        )
        print(query, file=stderr)
        try:
            cur.execute(query)
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Duplicate entry for medic"}, 400)
        mysql.connection.commit()
        cur.close()
        return make_response({"message": "Success!"}, 201)
    elif request.method == "DELETE":
        data_received = request.get_json()
        if not validate_json(["username"], data_received):
            cur.close()
            return make_response({"message": "Invalid json"}, 400)
        medic_id = get_login_id(data_received["username"])
        if medic_id == -1:
            cur.close()
            return make_response({"message": "Bad username"}, 400)
        query = """
        DELETE FROM MEDIC_DETAILS WHERE ID = '{}';
        """.format(medic_id)
        cur.execute(query)
        affected_rows = cur.rowcount
        if affected_rows == 0:
            cur.close()
            return make_response({"message": "Medic is not in list"}, 400)
        mysql.connection.commit()
        cur.close()
        return make_response({"message": "Successfully deleted user " + data_received["username"]}, 201)
    return ""

@app.route("/medic_reviews/<medic_username>", methods = ["GET", "POST", "DELETE"])
def medic_reviews(medic_username):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        medic_id = get_login_id(medic_username)
        if medic_id == -1:
            return make_response({"message": "Bad username"}, 400)
        cur.execute("SELECT REVIEW, IMAGE_STAMP FROM REVIEWS WHERE ID = '{}".format(medic_id))
        response_db = cur.fetchall()
        if response_db is not None:
            list_of_reviews = []
            for entry in response_db:
                list_of_reviews.append({"review": entry[1], "image_path": "/images/" + entry[2]})
            cur.close()
            return make_response(json.dumps(list_of_reviews), 200)
        cur.close()
        return make_response({"message": "No reviews found for username " + medic_username}, 400)
    if request.method == "POST":
        data_received = request.get_json()
        if not validate_json(["review"], data_received):
            cur.close()
            return make_response({"message": "Invalid json"}, 400)
        medic_id = get_login_id(medic_username)
        if medic_id == -1:
            cur.close()
            return make_response({"message": "Bad username"}, 400)
        try:
            timestamp = datetime.fromtimestamp(time.time())\
                                                    .strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("""INSERT INTO REVIEWS    ( MEDIC_ID,
                                                    REVIEW,
                                                    IMAGE_STAMP)
                            VALUES ({medic_id}, {review}, {image_stamp})"""
                        .format(
                            medic_id    = medic_id,
                            review      = format_sql(data_received["review"]),
                            image_stamp = format_sql(timestamp)
                        ))
            mysql.connection.commit()
            cur.close()
            return make_response({"message": "Review added successfully", "timestamp": \
                                  str(timestamp.replace(" ", "+"))}, 201)
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Database insertion error"}, 500)
    return ""

# medical data:
# - consultatii + tratament, donarea de sange + data