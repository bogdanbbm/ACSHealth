from __main__ import app, stderr, request, mysql, validate_json, abort, format_sql, make_response, json

@app.route("/images/<timestamp>", methods = ["GET", "POST"])
def get_image(timestamp :str):
    cur = mysql.connection.cursor()
    timestamp = timestamp.replace("+", " ")
    if request.method == "GET":
        try:
            cur.execute("SELECT PHOTO FROM IMAGES WHERE IMAGE_STAMP = '{}'"
                        .format(timestamp))
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Db selection error"}, 500)
        response_db = cur.fetchone()
        if response_db is not None:
            cur.close()
            return make_response(response_db[0], 200)
        cur.close()
        return make_response({"message": "Bad timestamp"}, 400)
    elif request.method == "POST":
        if 'file' not in request.files:
            cur.close()
            return make_response({"message": "No file provided"}, 400)
        cur.execute("SELECT ID_REVIEW FROM REVIEWS WHERE IMAGE_STAMP = '{}'"
                    .format(timestamp))
        response_db = cur.fetchone()
        review_id = -1
        if response_db is not None:
            review_id = response_db[0]
        if review_id == -1:
            return make_response({"message": "Invalid timestamp"}, 400)
        query = """
        INSERT INTO IMAGES (ID_REVIEW,
                            IMAGE_STAMP,
                            PHOTO)
        VALUES (%s, %s, %s);
        """
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            query_args = (review_id, timestamp, uploaded_file.read())
        else:
            cur.close()
            return make_response({"message": "No filename provided"}, 400)
        try:
            cur.execute(query, query_args)
            mysql.connection.commit()
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Db insertion error"}, 500)
        cur.close()
        return make_response({"message": "Image uploaded successfully"}, 201)
    return ""