from backend import validate_json, mysql, login_details
from flask import Blueprint, make_response, request
from sys import stderr
from uuid import uuid4
from email_module import compute_email
import jwt
from datetime import datetime, timedelta


identity_blueprint = Blueprint('identity', __name__)

@identity_blueprint.route('/register/<email_uid>', methods = ["GET"])
def process_verification(email_uid : str):
    """
    The first 15 chars are reserved for the database id,
    the rest are the uuid for the email
    """
    print("id-ul", email_uid, file=stderr)
    user = login_details.query.filter_by(mail_uuid=email_uid).first()
    if user.mail_uuid != None:
        user.mail_check = 'Y'
        mysql.session.commit()
        check = login_details.query.filter_by(mail_uuid=email_uid).first()
        print(check.mail_check, file=stderr)
        return "<p style=\"position: fixed;top: 50%;left: 50%;\">Toutes mes felicitations monsieur!</p>"
    else:
        return make_response({"message": "Bad uuid"}, 400)

@identity_blueprint.route('/register', methods = ["POST"])
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
    id = None
    try:
        id = login_details.query.filter_by(username=data_received["username"]).first()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Db selection error"}, 500)
    if id is not None:
        # it exists already
        return make_response({"message": "Username already exists"}, 400)
    user = login_details(data_received["username"], data_received["password"],\
                        'Y' if int(data_received["isMedic"]) == 1 else 'N', str(generated_uuid),\
                        'N' if int(data_received["isMedic"]) == 1 else 'Y')
    try:
        mysql.session.add(user)
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Db insertion error"}, 500)
    mysql.session.commit()
    compute_email(data_received["email"], generated_uuid)
    return make_response({"message": "Success"}, 201)

@identity_blueprint.route('/login', methods = ["POST"])
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
    user = login_details.query.filter_by(username=data_received["username"])\
                              .filter_by(password=data_received["password"]).first()
    if user is None:
        print("Account does not exist", file=stderr)
        return make_response({"message": "Account does not exist"}, 400)
    if user.mail_check != 'Y':
        print("Email not verified", file=stderr)
        return make_response({"message": "Email not verified"}, 400)
    print("Login successful!", file=stderr)
    token = jwt.encode({
        'isMedic': 0 if user.is_medic == 'N' else 1,
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
    }, "secret")
    return make_response({'token' : token}, 201)