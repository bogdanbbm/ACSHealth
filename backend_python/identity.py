from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from db_ops import get_login_id
from sys import stderr
from uuid import uuid4
from email_module import compute_email
import jwt
from models import login_details

identity_blueprint = Blueprint('identity', __name__)


@identity_blueprint.route('/register/<email_uid>', methods = ["GET"])
def process_verification(email_uid : str):
    """
    The first 15 chars are reserved for the database id,
    the rest are the uuid for the email
    """
    print("id-ul", email_uid, file=stderr)
    # query database for email
    user = login_details.query.filter_by(mail_uuid=email_uid).first()

    # if email exists, mark it as verified
    if user.mail_uuid != None:
        user.mail_check = 'Y'
        mysql.session.commit()
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
    # validate json and generate uuid
    generated_uuid = uuid4()
    data_received = request.get_json()
    if not validate_json(["email", "username", "password", "isMedic"], data_received):
        return make_response({"message": "Invalid json"}, 400)
    if int(data_received["isMedic"]) not in [0, 1]:
        return make_response({"message": "isMedic should be 0 or 1!"}, 400)
    if data_received["username"] == "" or data_received["password"] == "":
        return make_response({"message": "Username or password empty"}, 400)

    # check if account already exists
    id = None
    try:
        id = login_details.query.filter_by(username=data_received["username"]).first()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Db selection error"}, 500)
    if id is not None:
        return make_response({"message": "Username already exists"}, 400)

    # create user and insert it into database
    user = login_details(data_received["username"], data_received["password"],\
                        'Y' if int(data_received["isMedic"]) == 1 else 'N', str(generated_uuid),\
                        'N' if int(data_received["isMedic"]) == 1 else 'Y')
    try:
        mysql.session.add(user)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Db insertion error"}, 500)

    # send verification email
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
    # validate json
    data_received = request.get_json()
    if not validate_json(["username", "password"], data_received):
        return make_response({"message": "Invalid json"}, 400)
    if data_received["username"] == "" or data_received["password"] == "":
        return make_response({"message": "Username or password empty"}, 400)

    # query database for user
    user = login_details.query.filter_by(username=data_received["username"])\
                              .filter_by(password=data_received["password"]).first()

    # check whether account exists or not
    if user is None:
        print("Account does not exist", file=stderr)
        return make_response({"message": "Account does not exist"}, 400)

    # check whether user has verified email or not
    if user.mail_check != 'Y':
        print("Email not verified", file=stderr)
        return make_response({"message": "Email not verified"}, 400)

    # generate and return jwt for user
    print("Login successful!", file=stderr)
    token = token.encode('ascii', 'ignore')
    token = jwt.encode(payload={"username":user.username}, key="secret")
    return make_response({'token' : token}, 201)


@identity_blueprint.route("/has_completed", methods=["GET"])
def has_completed():
    token = token.encode('ascii', 'ignore')
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

    # get id for provided username to check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # query database for user and return whether they have completed personal data or not
    user = login_details.query.filter_by(id=login_id).first()
    completed = 1 if user.completed_reg == 'Y' else 0
    return make_response({"completed":completed}, 200)


@identity_blueprint.route("/is_medic", methods=["GET"])
def is_medic():
    token = token.encode('ascii', 'ignore')
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

    # get id for provided username to check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    user = login_details.query.filter_by(id=login_id).first()
    med = True if user.is_medic == 'Y' else False
    return make_response(med, 200)
