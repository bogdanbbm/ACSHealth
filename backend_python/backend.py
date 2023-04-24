from flask import Flask, request, abort, make_response, jsonify
import jwt
from datetime import datetime, timedelta
from flask_mysqldb import MySQL
from flask_cors import CORS
from sys import stderr
from email_module import compute_email
from uuid import uuid4

app = Flask(__name__)

# Configure MySQL connection
# TODO: get these from env
app.config['MYSQL_HOST'] = 'mysql-database'
app.config['MYSQL_USER'] = 'prod'
app.config['MYSQL_PASSWORD'] = 'something_encrypt3d'
app.config['MYSQL_DB'] = 'ip'

mysql = MySQL(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def format_sql(command):
    """
    This just helps with strings in sql commands
    """
    return "\'" + command + "\'"
 
def validate_json(list_of_fields, json):
    """
    Check if json has the right fields
    """
    for field in list_of_fields:
        if field not in json:
            return False
    return True
 
@app.route('/register/<email_uid>', methods = ["GET"])
def process_verification(email_uid : str):
    """
    The first 15 chars are reserved for the database id,
    the rest are the uuid for the email
    """
    if request.method == "GET":
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
            abort(404)
 
 
@app.route('/register', methods = ["POST"])
def register():
    """
    This method will receive a JSON containing
    the following entries:
    email           -> str
    username        -> str
    pass_hash       -> str (sha256)
    is_medic        -> int (either 0 or 1)
    """
 
    if request.method == 'POST':
        generated_uuid = uuid4()
        data_received = request.get_json()
        if not validate_json(["email", "username", "pass_hash", "is_medic"], data_received):
            abort(404)
        if int(data_received["is_medic"]) not in [0, 1]:
            abort(404)
        if data_received["username"] == "" or data_received["pass_hash"] == "":
            abort(404)
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO LOGIN_DETAILS   (USERNAME,
                                        PASS_HASH,
                                        IS_MEDIC,
                                        MAIL_UUID)
                VALUES ({username},
                        {pass_hash}, {is_medic},
                        {mail_uuid});
        """.format(
            username    = format_sql(data_received["username"]),
            pass_hash   = format_sql(data_received["pass_hash"]),
            is_medic    = int(data_received["is_medic"]),
            mail_uuid   = format_sql(str(generated_uuid))
        )
        print(query, file=stderr)
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        compute_email(data_received["email"], generated_uuid)
    return ""

@app.route('/login', methods = ["POST"])
def login():
    """
    This method will receive a JSON containing
    the following entries:
    username        -> str
    pass_hash       -> str (sha256)
    """
 
    if request.method == 'POST':
        data_received = request.get_json()
        if not validate_json(["username", "pass_hash"], data_received):
            abort(404)
        if data_received["username"] == "" or data_received["pass_hash"] == "":
            abort(404)
        cur = mysql.connection.cursor()
        query = """
            SELECT IS_MEDIC, MAIL_CHECK
            FROM LOGIN_DETAILS
            WHERE USERNAME = {username} AND PASS_HASH = {pass_hash};
        """.format(
            username    = format_sql(data_received["username"]),
            pass_hash   = format_sql(data_received["pass_hash"]),
        )
        print(query, file=stderr)
        cur.execute(query)
        query_res = cur.fetchall()[0]
        print(query_res, file=stderr)
        if query_res != None:
            if query_res[1] != 'Y':
                print("Login failed", file=stderr)
                cur.close()
                return make_response({"message": "Login failed"}, 401)
            print("Login successful!", file=stderr)
            token = jwt.encode({
                'is_medic': int(query_res[0]),
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, "secret")
            cur.close()
            return make_response(jsonify({'token' : token}), 201)
        else:
            print("Login failed", file=stderr)
            cur.close()
            return make_response({"message": "Login failed"}, 401)
    return ""

if __name__ == '__main__':
    # TODO: when running in prod delete debug=True
    app.run(host='0.0.0.0', port=5000, debug=True)