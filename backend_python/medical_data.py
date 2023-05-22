
from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from db_ops import get_login_id
from sys import stderr
from datetime import datetime
from models import login_details, medic_details, consultations
from json import dumps

medical_data_blueprint = Blueprint("medical_data", __name__)


@medical_data_blueprint.route("/medical_data/<patient_username>", methods = ["GET"])
def get_medical_data(patient_username):
    # get id for provided username to check if it exists
    login_id = get_login_id(patient_username)
    if login_id == -1:
        return make_response({"message": "Bad username"}, 400)

    # query database for all consultations for the patient
    cons_res = consultations.query.filter_by(id_patient=login_id).all()
    if cons_res == []:
        return make_response({"message": "No consultations found"}, 204)
    cons_list = []
    for cons in cons_res:
        # compute list of consultations and return it
        
        med = login_details.query.filter_by(id=cons.id_medic).first()
        # if at any point a medic for one of the consultations hasn't completed
        # the registration process return an error
        if med.completed_reg == 'N':
            return make_response(dumps({"message": "Medic has not completed personal data"}), 400)
        
        medd = medic_details.query.filter_by(id=cons.id_medic).first()
        med_name = medd.fname + " " + medd.lname
        cons_list.append({"medic": med_name,
                          "date":str(cons.consult_date), "treatment":cons.treatment})
    
    return make_response(dumps(cons_list), 200)


@medical_data_blueprint.route("/medical_data/<medic_username>", methods = ["POST"])
def post_medical_data(medic_username):
    # validate json
    data_received = request.get_json()
    if not validate_json(["patientUsername", "treatment", "consultationDate"],
                            data_received):
        return make_response({"message": "Invalid json"}, 400)

    # get id for provided username to check if it exists
    login_id = get_login_id(medic_username)
    if login_id == -1:
        return make_response({"message": "Bad username"}, 400)
    
    # get id for provided patient to check if it exists
    patient_id = get_login_id(data_received["patientUsername"])
    if patient_id == -1:
        return make_response({"message": "Bad request"}, 400)
    
    # check if user is medic and deny permission if not
    user = login_details.query.filter_by(username=medic_username).first()
    if user is not None and user.is_medic == 'N':
        return make_response({"message": "Permission denied"}, 403)
    
    # insert consultation into database
    try:
        date = datetime.strptime(data_received["consultationDate"], "%d/%m/%Y")
        cons = consultations(login_id, patient_id, date.strftime('%Y-%m-%d %H:%M:%S'),
                            data_received["treatment"])
        mysql.session.add(cons)
        mysql.session.commit()
        return make_response({"message": "Consultation added successfully"}, 201)
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Database insertion error"}, 500)