from flask import Blueprint, make_response, request
from models import patient_data, allergy_list, login_details
from utils import mysql, validate_json
from db_ops import get_login_id
from sys import stderr
from datetime import datetime
import jwt

patient_data_blueprint = Blueprint("patient_data", __name__)

@patient_data_blueprint.route('/patient_data', methods=["GET"])
def get_personal_data():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])
    
    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # create object with mandatory data and potentially optional data that has been completed
    data = patient_data.query.filter_by(id=login_id).first()
    if data is not None:
        data_obj = {}
        data_obj["firstName"] = data.first_name
        data_obj["lastName"] = data.last_name
        data_obj["cnp"] = data.cnp
        data_obj["sex"] = data.gender
        data_obj["birthdate"] = str(data.birthdate)
        if data.height is not None:
            data_obj["height"] = data.height
        if data.weight is not None:
            data_obj["weight"] = data.weight
        if data.sgroup is not None:
            data_obj["bloodGroup"] = data.sgroup
        if data.rh is not None:
            data_obj["RH"] = data.rh

        # add allergy list to the object
        allergy_res = allergy_list.query.filter_by(patient_id=login_id).all()
        allergies = []
        for allergy in allergy_res:
            allergies.append({"allergy":allergy.allergy})
        data_obj["allergies"] = allergies

        return make_response(data_obj, 200)
    return make_response({}, 204)


@patient_data_blueprint.route("/patient_data", methods=["POST"])
def insert_personal_data():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

    data_received = request.get_json()
    personal_data = None

    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # validate json
    if validate_json(["firstName", "lastName", "cnp", "sex", "birthdate"], data_received):
        # create object with mandatory data
        try:
            date = datetime.strptime(data_received["birthdate"], "%Y-%m-%d")
            personal_data = patient_data(login_id,
                                        data_received["firstName"],
                                        data_received["lastName"],
                                        data_received["cnp"],
                                        date.strftime('%Y-%m-%d %H:%M:%S'),
                                        data_received["sex"])
            mysql.session.add(personal_data)

            pat = login_details.query.filter_by(id=login_id).first()
            pat.completed_reg = 'Y'
            
            mysql.session.commit()
        except Exception as e:
            print(e, file=stderr)
            return make_response({"message":"Database insertion error"}, 500)
    else:
        return make_response({"message":"Invalid JSON"}, 400)
    
    # check if object has been inserted by query-ing database
    pers = patient_data.query.filter_by(id=login_id).first()

    # check if any optional data has been completed
    try:
        if validate_json(["weight"], data_received):
            pers.weight = float(data_received["weight"])
        if validate_json(["height"], data_received):
            pers.height = float(data_received["height"])
        if validate_json(["bloodGroup"], data_received):
            pers.sgroup = data_received["bloodGroup"]
        if validate_json(["RH"], data_received):
            pers.rh = data_received["RH"]
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database insertion error"}, 500)
    
    return make_response({"message":"Successfully added patient data"}, 201)


@patient_data_blueprint.route("/patient_data", methods=["PATCH"])
def update_personal_data():
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])
    data_received = request.get_json()

    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # query database for the patient
    pers = patient_data.query.filter_by(id=login_id).first()
    if pers is None:
        return make_response({"message":"Not completed mandatory data"}, 400)

    # update values for received optional fields
    try:
        if validate_json(["weight"], data_received):
            pers.weight = float(data_received["weight"])
        if validate_json(["height"], data_received):
            pers.height = float(data_received["height"])
        if validate_json(["bloodGroup"], data_received):
            pers.sgroup = data_received["bloodGroup"]
        if validate_json(["RH"], data_received):
            pers.rh = data_received["RH"]
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database update error"}, 500)
    
    return make_response({"message":"Successfully updated patient data"}, 200)

@patient_data_blueprint.route("/patient_data/allergies", methods=["POST"])
def insert_allergy():
    data_received = request.get_json()
    token = jwt.decode(jwt=request.headers.get('Authorization'), key="secret", algorithms=["HS256"])

    # get id from username and check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # validate json
    if not validate_json(["allergy"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    # insert allergy into database
    try:
        allergy = allergy_list(login_id, data_received["allergy"])
        mysql.session.add(allergy)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database insertion error"}, 500)
    
    return make_response({"message":"Successfully added allergy"}, 201)