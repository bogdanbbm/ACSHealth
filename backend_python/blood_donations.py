from flask import Blueprint, make_response, request
from models import blood_donation_history
from utils import mysql, validate_json
from sys import stderr
from db_ops import get_login_id
import jwt
from json import dumps
from datetime import datetime

blood_donations_blueprint = Blueprint("blood_donations", __name__)


@blood_donations_blueprint.route("/blood_donations", methods=["GET"])
def get_blood_donations():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])
    
    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # query database for all blood donations for the user
    donations_res = blood_donation_history.query.filter_by(patient_id=login_id).all()
    if donations_res == []:
        return make_response({}, 204)
    
    # if there are any donations, add them to a list and return it
    donation_list = []
    for donation in donations_res:
        donation_list.append({"donationDate":str(donation.donation_date)})
    
    return make_response(dumps(donation_list), 200)


@blood_donations_blueprint.route("/blood_donations", methods=["POST"])
def insert_blood_donation():
    data_received = request.get_json()
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])
    
    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)

    # validate json
    if not validate_json(["donationDate"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    # insert blood donation into database
    try:
        date = datetime.strptime(data_received["donationDate"], "%d/%m/%Y")
        donation = blood_donation_history(login_id, date.strftime('%Y-%m-%d %H:%M:%S'))
        
        mysql.session.add(donation)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database insertion error"}, 500)
    
    return make_response({"message":"Successfully added blood donation record"}, 201)