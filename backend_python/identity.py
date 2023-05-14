from __main__ import app, stderr, request, mysql, validate_json, abort, format_sql, make_response, \
uuid4, compute_email, jwt, datetime, timedelta, jsonify

@app.route('/register/<email_uid>', methods = ["GET"])
def process_verification(email_uid : str):
    """
    The first 15 chars are reserved for the database id,
    the rest are the uuid for the email
    """
    cur = mysql.connection.cursor()
    print("id-ul", email_uid, file=stderr)
    cur.execute("SELECT MAIL_UUID FROM LOGIN_DETAILS WHERE MAIL_UUID = '{}'"
                .format(email_uid))
    if cur.fetchone()[0] != None:
        query = """
            UPDATE LOGIN_DETAILS
            SET MAIL_CHECK = 'Y'
            WHERE   MAIL_UUID = '{id_given}';
        """.format(
            id_given = email_uid
        )
        cur.execute(query)
        mysql.connection.commit()
        # test that it works:
        cur.execute("SELECT * FROM LOGIN_DETAILS WHERE MAIL_UUID = '{}'".format(email_uid))
        print(cur.fetchone(), file=stderr)
        cur.close()
        return "<p style=\"position: fixed;top: 50%;left: 50%;\">Toutes mes felicitations monsieur!</p>"
    else:
        return make_response({"message": "Bad uuid"}, 400)
 
 
@app.route('/register', methods = ["POST"])
def register():
    """
    This method will receive a JSON containing
    the following entries:
    email           -> str
    username        -> str
    password       -> str (sha256)
    isMedic        -> int (either 0 or 1)
    """
    generated_uuid = uuid4()
    data_received = request.get_json()
    if not validate_json(["email", "username", "password", "isMedic"], data_received):
        return make_response({"message": "Invalid json"}, 400)
    if int(data_received["isMedic"]) not in [0, 1]:
        return make_response({"message": "isMedic should be 0 or 1!"}, 400)
    if data_received["username"] == "" or data_received["password"] == "":
        return make_response({"message": "Username or password empty"}, 400)
    cur = mysql.connection.cursor()
    # check whether the username is taken or not
    try:
        cur.execute("SELECT ID FROM LOGIN_DETAILS WHERE USERNAME = '{}'"
                .format(data_received["username"]))
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message": "Db selection error"}, 500)
    db_response = cur.fetchone()
    if db_response is not None:
        # it exists already
        cur.close()
        return make_response({"message": "Username already exists"}, 400)
    query = """
        INSERT INTO LOGIN_DETAILS   (USERNAME,
                                    PASS_HASH,
                                    IS_MEDIC,
                                    MAIL_UUID)
            VALUES ({username},
                    {password}, {isMedic},
                    {mail_uuid});
    """.format(
        username    = format_sql(data_received["username"]),
        password   = format_sql(data_received["password"]),
        isMedic    = format_sql('Y' if int(data_received["isMedic"]) == 1 else 'N'),
        mail_uuid   = format_sql(str(generated_uuid))
    )
    print(query, file=stderr)
    try:
        cur.execute(query)
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message":"Db insertion error"}, 500)
    mysql.connection.commit()
    cur.close()
    compute_email(data_received["email"], generated_uuid)
    return make_response({"message": "Success"}, 201)

@app.route('/login', methods = ["POST"])
def login():
    """
    This method will receive a JSON containing
    the following entries:
    username        -> str
    password       -> str (sha256)
    """
    data_received = request.get_json()
    if not validate_json(["username", "password"], data_received):
        return make_response({"message": "Invalid json"}, 400)
    if data_received["username"] == "" or data_received["password"] == "":
        return make_response({"message": "Username or password empty"}, 400)
    cur = mysql.connection.cursor()
    query = """
        SELECT IS_MEDIC, MAIL_CHECK
        FROM LOGIN_DETAILS
        WHERE USERNAME = {username} AND PASS_HASH = {password};
    """.format(
        username    = format_sql(data_received["username"]),
        password   = format_sql(data_received["password"]),
    )
    print(query, file=stderr)
    cur.execute(query)
    query_res = cur.fetchall()[0]
    print(query_res, file=stderr)
    if query_res != None:
        if query_res[1] != 'Y':
            print("Login failed1", file=stderr)
            cur.close()
            return make_response({"message": "Login failed1"}, 400)
        print("Login successful!", file=stderr)
        token = jwt.encode({
            'isMedic': 0 if query_res[0] == 'N' else 1,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, "secret")
        cur.close()
        return make_response(jsonify({'token' : token}), 201)
    else:
        print("Login failed2", file=stderr)
        cur.close()
        return make_response({"message": "Login failed2"}, 400)