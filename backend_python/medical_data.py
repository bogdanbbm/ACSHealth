
from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from db_ops import get_login_id
from sys import stderr
from datetime import datetime
from models import login_details, medic_details, consultations
from json import dumps
import jwt

medical_data_blueprint = Blueprint("medical_data", __name__)


@medical_data_blueprint.route("/medical_data", methods = ["GET"])
def get_medical_data():
    token = jwt.decode(jwt=request.headers.get('Authorization').split(" ")[1],
                        key="secret", algorithms=["HS256"])

    # get id for provided username to check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message": "Bad username"}, 400)
    
    # check if medic and return appropriate consultation list if that is the case
    user = login_details.query.filter_by(username=token.get('username')).first()
    if user is not None and user.is_medic == 'Y':
        cons_ress = consultations.query.filter_by(id_medic=login_id).all()
        if cons_ress == []:
            return make_response({}, 204)
        
        cons_l = []
        for cons in cons_ress:
            # compute list of consultations and return it
            pat = login_details.query.filter_by(id=cons.id_patient).first()
            cons_l.append({"patientUsername": pat.username,
                            "consultationDate":str(cons.consult_date), "treatment":cons.treatment})
            
        return make_response(dumps(cons_l), 200)

    # query database for all consultations for the patient
    cons_res = consultations.query.filter_by(id_patient=login_id).all()
    if cons_res == []:
        return make_response({}, 204)

    cons_list = []
    for cons in cons_res:
        # compute list of consultations and return it
        
        med = login_details.query.filter_by(id=cons.id_medic).first()
        # if at any point a medic for one of the consultations hasn't completed
        # the registration process return an error
        cons_list.append({"medicUsername": med.username,
                          "consultationDate":str(cons.consult_date), "treatment":cons.treatment})
    
    return make_response(dumps(cons_list), 200)


@medical_data_blueprint.route("/medical_data", methods = ["POST"])
def post_medical_data():
    token = jwt.decode(jwt=request.headers.get('Authorization').split(" ")[1],
                        key="secret", algorithms=["HS256"])
    
    # validate json
    data_received = request.get_json()
    if not validate_json(["patientUsername", "treatment", "consultationDate"],
                            data_received):
        return make_response({"message": "Invalid json"}, 400)

    # get id for provided username to check if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message": "Bad username"}, 400)
    
    # get id for provided patient to check if it exists
    patient_id = get_login_id(data_received["patientUsername"])
    if patient_id == -1:
        return make_response({"message": "Bad request"}, 400)
    
    # check if user is medic and deny permission if not
    user = login_details.query.filter_by(username=token.get('username')).first()
    if user is not None and user.is_medic == 'N':
        return make_response({"message": "Permission denied"}, 403)
    
    # insert consultation into database
    try:
        date = datetime.strptime(data_received["consultationDate"], "%Y-%m-%d")
        cons = consultations(login_id, patient_id, date.strftime('%Y-%m-%d %H:%M:%S'),
                            data_received["treatment"])
        mysql.session.add(cons)
        mysql.session.commit()
        return make_response({"message": "Consultation added successfully"}, 201)
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Database insertion error"}, 500)