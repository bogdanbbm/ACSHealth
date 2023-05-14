from __main__ import app, mysql, validate_json, format_sql
from flask import request, make_response
from sys import stderr
import json
import time
from datetime import datetime
from sys import stderr
# all of these are used for imports in the different modules

def get_login_id(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID FROM LOGIN_DETAILS WHERE USERNAME = '{}'"
                    .format(username))
    login_id = -1
    response_db = cur.fetchone()
    if response_db is not None and response_db[0] is not None:
        login_id = int(response_db[0])
    return login_id

@app.route("/medic_list", methods = ["GET"])
def get_medic_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT FNAME, LNAME, RATING, IMAGE_STAMP FROM MEDIC_DETAILS")
    response_db = cur.fetchall()
    if response_db is not None:
        list_of_medics = []
        for entry in response_db:
            list_of_medics.append({"fname": entry[0], "lname": entry[1],
                                "rating": "{:.2f}".format(float(entry[2])) if entry[2] is not None else 0,
                                "image_stamp": str(entry[3]).replace(" ", "+")})
        cur.close()
        return make_response(json.dumps(list_of_medics), 200)
    cur.close()
    return make_response({"message": "No medics found"}, 400)

@app.route("/medic_list", methods = ["POST"])
def post_medic_details():
        cur = mysql.connection.cursor()
        data_received = request.get_json()
        if not validate_json(["username", "fname", "lname"], data_received):
            cur.close()
            return make_response({"message": "Invalid json"}, 400)
        cur.execute("SELECT ID FROM LOGIN_DETAILS WHERE USERNAME = '{}'"
                    .format(data_received["username"]))
        medic_id = get_login_id(data_received["username"])
        if medic_id == -1:
            return make_response({"message": "Bad username"}, 400)
        timestamp = datetime.fromtimestamp(time.time())\
                                                    .strftime('%Y-%m-%d %H:%M:%S')
        query = """
        INSERT INTO MEDIC_DETAILS (ID, FNAME,
                                    LNAME,
                                    RATING,
                                    IMAGE_STAMP)
            VALUES ({medic_id}, {fname},
                    {lname}, {rating}, {stamp});
        """.format(
            medic_id    = medic_id,
            fname       = format_sql(data_received["fname"]),
            lname       = format_sql(data_received["lname"]),
            rating      = 'NULL',
            stamp       = format_sql(timestamp)
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
        return make_response({"message": "Success!", "timestamp": str(timestamp.replace(" ", "+"))}, 201)

@app.route("/medic_reviews/<medic_username>", methods = ["GET"])
def get_medic_reviews(medic_username):
    cur = mysql.connection.cursor()
    medic_id = get_login_id(medic_username)
    if medic_id == -1:
        cur.close()
        return make_response({"message": "Bad username"}, 400)
    cur.execute("SELECT REVIEW, RATING, ID_REVIEW FROM REVIEWS WHERE ID_MEDIC = '{}'".format(medic_id))
    response_db = cur.fetchall()
    if response_db is not None:
        list_of_reviews = []
        for entry in response_db:
            list_of_reviews.append({"review": entry[0], "rating": entry[1], "id": entry[2]})
        cur.close()
        return make_response(json.dumps(list_of_reviews), 200)
    cur.close()
    return make_response({"message": "No reviews found for username " + medic_username}, 400)

@app.route("/medic_reviews/<medic_username>", methods = ["POST"])
def post_medic_reviews(medic_username):
    cur = mysql.connection.cursor()
    data_received = request.get_json()
    if not validate_json(["review", "rating"], data_received):
        cur.close()
        return make_response({"message": "Invalid json"}, 400)
    medic_id = get_login_id(medic_username)
    if medic_id == -1:
        cur.close()
        return make_response({"message": "Bad username"}, 400)
    try:
        cur.execute("""INSERT INTO REVIEWS    ( ID_MEDIC,
                                                REVIEW,
                                                RATING)
                        VALUES ({medic_id}, {review}, {rating})"""
                    .format(
                        medic_id    = medic_id,
                        review      = format_sql(data_received["review"]),
                        rating      = float(data_received["rating"])
                    ))
        mysql.connection.commit()
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message": "Database insertion error"}, 500)
    # update medic rating
    try:
        cur.execute("UPDATE MEDIC_DETAILS \
                    SET RATING = \
                    (SELECT AVG(RATING) FROM REVIEWS WHERE ID_MEDIC = '{}')"
                    .format(get_login_id(medic_username)))
        mysql.connection.commit()
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message": "Database update error"}, 500)
    cur.close()
    return make_response({"message": "Review added successfully"}, 201)

@app.route("/medic_reviews", methods = ["DELETE"])
def delete_medic_reviews():
    cur = mysql.connection.cursor()
    data_received = request.get_json()
    if not validate_json(["review_id"], data_received):
        cur.close()
        return make_response({"message": "Invalid json"}, 400)
    try:
        cur.execute("SELECT ID_REVIEW FROM REVIEWS WHERE ID_REVIEW = '{}'"
                    .format(data_received["review_id"]))
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message": "Db selection error"}, 400)
    response_db = cur.fetchone()
    if response_db is not None:
        # delete from reviews
        try:
            cur.execute("DELETE FROM REVIEWS WHERE ID_REVIEW = '{}'".format(response_db[0]))
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Db deletion error"}, 400)
        mysql.connection.commit()
    else:
        cur.close()
        return make_response({"message": "Wrong review id"}, 400)
    return make_response({"message": "Success"}, 201)


# medical data:
# - consultatii + tratament, donarea de sange + data