from flask import Blueprint, make_response, request
from sys import stderr
from utils import mysql, validate_json
from models import payments, medic_details, login_details
from datetime import datetime
from db_ops import get_login_id
import jwt

payments_blueprint = Blueprint("payments", __name__)

@payments_blueprint.route('/payments', methods = ["GET"])
def get_payments():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

     # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    data = payments.query.filter_by(medic_id=login_id).all()
    print(data, file=stderr)
    if data is not None and data != []:
        response_obj = []
        for entry in data:
            data_obj = {}
            medic_details_obj = medic_details.query.filter_by(id = entry.medic_id).first()
            data_obj["firstName"]   = medic_details_obj.fname
            data_obj["lastName"]    = medic_details_obj.lname
            data_obj["value"]       = entry.value
            data_obj["paymentDate"] = entry.payment_date
            data_obj["patientUsername"] = entry.patient_username
            data_obj["currency"]    = entry.currency
            response_obj.append(data_obj)
        return make_response(response_obj, 200)
    return make_response({}, 204)

@payments_blueprint.route('/payments', methods = ["POST"])
def insert_payment():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

    data_received = request.get_json()
    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # validate json
    if validate_json(["value", "currency", "paymentDate", "patientUsername"], data_received):
        # create object with mandatory data
        try:
            date = data_received["paymentDate"] + " " + \
                str(datetime.now().strftime("%H:%M:%S"))
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            print(date.strftime('%Y-%m-%d %H:%M:%S'), file=stderr)
            new_payment = payments(medic_id = login_details.query.filter_by(id = login_id).first().id,
                                   value = data_received["value"],
                                   payment_date = date.strftime('%Y-%m-%d %H:%M:%S'),
                                   patient_username = data_received["patientUsername"],
                                   currency = data_received["currency"])
            mysql.session.add(new_payment)
            mysql.session.commit()
        except Exception as e:
            print(e, file=stderr)
            return make_response({"message":"Database insertion error"}, 500)
    else:
        return make_response({"message":"Invalid JSON"}, 400)
    return make_response({"message":"Successfully added patient data"}, 201)