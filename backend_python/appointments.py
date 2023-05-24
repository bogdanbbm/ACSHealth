from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from db_ops import get_login_id, get_username, get_clinic_name, get_clinic_id
from models import appointments
from json import dumps
from datetime import datetime

appointments_blueprint = Blueprint("appointments", __name__)


@appointments_blueprint.route("/appointments/<username>", methods=["GET"])
def get_appointments(username):
    login_id = get_login_id(username)
    if login_id == -1:
        return make_response({"message":"Bad username"}, 400)
    
    appointments_res = appointments.query.filter_by(id_patient=login_id).all()
    if appointments_res == []:
        return make_response({}, 204)
    
    appointment_list = []
    for appointment in appointments_res:
        medic_username = get_username(appointment.id_medic)
        clinic_name = get_clinic_name(appointment.id_clinic)

        appointment_list.append({"idAppointment": appointment.id_appointment,
                                 "medicUsername": medic_username,
                                 "clinicName": clinic_name,
                                 "appointmentDate": str(appointment.appointment_date)})
    return make_response(dumps(appointment_list), 200)


@appointments_blueprint.route("/appointments/<username>", methods=["POST"])
def create_appointment(username):
    data_received = request.get_json()
    if not validate_json(["clinicName", "medicUsername", "appointmentDate"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)
    patient_id = get_login_id(username)
    if patient_id == -1:
        return make_response({"message": "Bad username"}, 400)

    try:
        clinic_id = get_clinic_id(data_received["clinicName"])
        medic_id = get_login_id(data_received["medicUsername"])
        date = datetime.strptime(data_received["appointmentDate"], "%d/%m/%Y")
        appointment = appointments(clinic_id, medic_id, patient_id, date.strftime('%Y-%m-%d %H:%M:%S'))

        mysql.session.add(appointment)
        mysql.session.commit()
    except Exception as e:
        return make_response({"message":"Database insertion error"}, 500)
    
    return make_response({"message":"Successfully created appointment"}, 201)


@appointments_blueprint.route("/appointments/<appointment_id>", methods=["PATCH"])
def modify_appointment(appointment_id):
    data_received = request.get_json()
    if not validate_json(["appointmentDate"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    try:
        appointment = appointments.query.filter_by(id_appointment=appointment_id).first()
        if appointment is None:
            return make_response({"message":"Invalid appointment id"}, 400)
        
        new_date = datetime.strptime(data_received["appointmentDate"], "%d/%m/%Y")
        appointment.appointment_date = new_date.strftime('%Y-%m-%d %H:%M:%S')
        mysql.session.commit()
    except Exception as e:
        return make_response({"message": "Database update error"}, 500)
    
    return make_response({"message":"Successfully changed appointment date"}, 200)