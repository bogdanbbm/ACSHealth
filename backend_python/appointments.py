from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from db_ops import get_login_id, get_username, get_clinic_name, get_clinic_id
from models import appointments, login_details
from json import dumps
from datetime import datetime
import jwt
from sys import stderr

appointments_blueprint = Blueprint("appointments", __name__)


@appointments_blueprint.route("/appointments", methods=["GET"])
def get_appointments():
    token = jwt.decode(jwt=request.headers.get('Authorization').split(" ")[1],
                        key="secret", algorithms=["HS256"])

    # get id for user and verify if it exists
    login_id = get_login_id(token.get('username'))
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    # check if user is medic and return the appropriate appointments
    user = login_details.query.filter_by(id=login_id).first()
    if user.is_medic == 'Y':
        # query database for all appoinments for the medic
        appointments_r = appointments.query.filter_by(id_medic=login_id).all()
        if appointments_r == []:
            return make_response({}, 204)
        
        # if there are appointments, create a list with their data and return it
        appointment_l = []
        for appointment in appointments_r:
            patient_username = get_username(appointment.id_patient)
            clinic_name = get_clinic_name(appointment.id_clinic)

            appointment_l.append({"idAppointment": appointment.id_appointment,
                                  "patientUsername": patient_username,
                                  "clinicName": clinic_name,
                                  "appointmentDate": str(appointment.appointment_date)})
        return make_response(dumps(appointment_l), 200)

    # query database for all appoinments for the patient
    appointments_res = appointments.query.filter_by(id_patient=login_id).all()
    if appointments_res == []:
        return make_response({}, 204)

    # if there are appointments, create a list with their data and return it
    appointment_list = []
    for appointment in appointments_res:
        medic_username = get_username(appointment.id_medic)
        clinic_name = get_clinic_name(appointment.id_clinic)

        appointment_list.append({"idAppointment": appointment.id_appointment,
                                 "medicUsername": medic_username,
                                 "clinicName": clinic_name,
                                 "appointmentDate": str(appointment.appointment_date)})
    return make_response(dumps(appointment_list), 200)


@appointments_blueprint.route("/appointments", methods=["POST"])
def create_appointment():
    token = jwt.decode(jwt=request.headers.get('Authorization').split(" ")[1],
                        key="secret", algorithms=["HS256"])

    # validate json
    data_received = request.get_json()
    if not validate_json(["clinicName", "medicUsername", "appointmentDate"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    # get id for user and verify if it exists
    patient_id = get_login_id(token.get('username'))
    if patient_id == -1:
        return make_response({"message": "Bad username"}, 400)

    # create appointment and insert it into database
    try:
        clinic_id = get_clinic_id(data_received["clinicName"])
        medic_id = get_login_id(data_received["medicUsername"])
        date = datetime.strptime(data_received["appointmentDate"], "%Y-%m-%d")
        appointment = appointments(clinic_id, medic_id, patient_id, date.strftime('%Y-%m-%d %H:%M:%S'))

        mysql.session.add(appointment)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database insertion error"}, 500)
    
    return make_response({"message":"Successfully created appointment"}, 201)


@appointments_blueprint.route("/appointments/<appointment_id>", methods=["PATCH"])
def modify_appointment(appointment_id):
    # validate json
    data_received = request.get_json()
    if not validate_json(["appointmentDate"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    # update date field in the appointment
    try:
        appointment = appointments.query.filter_by(id_appointment=appointment_id).first()

        # check if specified appointment exists
        if appointment is None:
            return make_response({"message":"Invalid appointment id"}, 400)

        new_date = datetime.strptime(data_received["appointmentDate"], "%Y-%m-%d")
        appointment.appointment_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
        mysql.session.commit()
    except Exception as e:
        return make_response({"message": "Database update error"}, 500)
    
    return make_response({"message":"Successfully changed appointment date"}, 200)

@appointments_blueprint.route("/appointments/<appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment = appointments.query.filter_by(id_appointment=appointment_id).first()

    if appointment is None:
        return make_response({"message":"Invalid appointment ID"}, 400)
    
    try:
        mysql.session.delete(appointment)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message":"Database deletion error"}, 500)
    
    return make_response({"message":"Successfully removed appointment"}, 200)