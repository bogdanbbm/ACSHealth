from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from json import dumps
from sys import stderr
from models import clinics

clinics_blueprint = Blueprint("clinics", __name__)


@clinics_blueprint.route("/clinics", methods=["GET"])
def get_clinics():
    # query database for all clinics
    clinics_res = clinics.query.all()

    # check if there are any clinics
    if clinics_res != []:
        clinics_list = []

        # compute clinic list and return it
        for clinic in clinics_res:
            clinics_list.append({"clinicName":clinic.name_clinic})
        return make_response(dumps(clinics_list), 200)
    
    return make_response({}, 204)

@clinics_blueprint.route("/clinics", methods=["POST"])
def add_clinic():
    # validate json
    data_received = request.get_json()
    if not validate_json(["clinicName"], data_received):
        return make_response({"message":"Invalid JSON"}, 400)

    # insert clinic into database
    try:
        clinic = clinics(data_received["clinicName"])
        mysql.session.add(clinic)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Database insertion error"}, 500)

    return make_response({"message":"Clinic successfully inserted"}, 201)