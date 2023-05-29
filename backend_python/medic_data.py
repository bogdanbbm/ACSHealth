from flask import Blueprint, make_response, request
from utils import mysql, validate_json
from sys import stderr
from datetime import datetime
from models import medic_details, reviews, login_details
from db_ops import get_login_id, get_username
from json import dumps
import time
import jwt
from sqlalchemy.sql import func

medic_blueprint = Blueprint("medics", __name__)


@medic_blueprint.route("/medic_list", methods = ["GET"])
def get_medic_details():
    # query database for all medics
    medics = medic_details.query.all()
    if medics != []:
        list_of_medics = []

        # compute list of medics
        for entry in medics:
            list_of_medics.append({"firstName": entry.fname, "lastName": entry.lname,
                                "rating": "{:.2f}".format(float(entry.rating)) if entry.rating is not None else 0,
                                "username": get_username(entry.id),
                                "imageStamp": str(entry.image_stamp).replace(" ", "+")})
        return make_response(dumps(list_of_medics), 200)

    return make_response({}, 204)


@medic_blueprint.route("/medic_list", methods = ["POST"])
def post_medic_details():
        token = jwt.decode(jwt=request.headers.get('Authorization').split(" ")[1],
                        key="secret", algorithms=["HS256"])

        # validate json
        data_received = request.get_json()
        if not validate_json(["firstName", "lastName"], data_received):
            return make_response({"message": "Invalid json"}, 400)

        # get id for provided username to check if it exists
        medic_id = get_login_id(token.get('username'))
        if medic_id == -1:
            return make_response({"message": "Bad username"}, 400)

        # generate a timestamp for future use with image uploading
        timestamp = datetime.fromtimestamp(time.time())\
                                                    .strftime('%Y-%m-%d %H:%M:%S')
        # insert medic info into database
        try:
            # TODO: get clinic id from front-end
            medic_info = medic_details(medic_id, data_received["firstName"],
                                       data_received["lastName"], mysql.sql.null(), timestamp)
            mysql.session.add(medic_info)
            med = login_details.query.filter_by(id=medic_id).first()
            med.completed_reg = 'Y'
            mysql.session.commit()
        except Exception as e:
            print(e, file=stderr)
            return make_response({"message": "Duplicate entry for medic"}, 400)

        return make_response({"message": "Success!", "timestamp": str(timestamp.replace(" ", "+"))}, 201)


@medic_blueprint.route("/medic_reviews/<medic_username>", methods = ["GET"])
def get_medic_reviews(medic_username):
    # get id for provided username to check if it exists
    medic_id = get_login_id(medic_username)
    if medic_id == -1:
        return make_response({"message": "Bad username"}, 400)

    # query database for all of the medic's reviews
    all_revs = reviews.query.filter_by(id_medic=medic_id).all()

    # check if there are any reviews
    if all_revs == []:
        return make_response({}, 204)

    list_of_reviews = []
    # compute the list of reviews and return it
    for entry in all_revs:
        list_of_reviews.append({"review": entry.review, "rating": entry.rating, "idReview": entry.id_review})
    return make_response(dumps(list_of_reviews), 200)


@medic_blueprint.route("/medic_reviews/<medic_username>", methods = ["POST"])
def post_medic_reviews(medic_username):
    # validate json
    data_received = request.get_json()
    if not validate_json(["review", "rating"], data_received):
        return make_response({"message": "Invalid json"}, 400)

    # get id for provided username to check if it exists
    medic_id = get_login_id(medic_username)
    if medic_id == -1:
        return make_response({"message": "Bad username"}, 400)

    # add review to the database
    try:
        rev = reviews(medic_id, data_received["review"], float(data_received["rating"]))
        mysql.session.add(rev)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Database insertion error"}, 500)

    # recalculate medic's average rating to account for the new review
    try:
        med = medic_details.query.filter_by(id=medic_id).first()

        new_rating = mysql.session.query(func.avg(reviews.rating).label('average'))\
                    .filter(reviews.id_medic==medic_id)
        med.rating = new_rating

        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Database update error"}, 500)

    return make_response({"message": "Review added successfully"}, 201)


@medic_blueprint.route("/medic_reviews/<id_review>", methods = ["DELETE"])
def delete_medic_reviews(id_review):
    # query the database for wanted review
    rev = None
    try:
        rev = reviews.query.filter_by(id_review=id_review).first()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Db selection error"}, 400)

    # check if the review exists and if it does remove it
    if rev is not None:
        try:
            mysql.session.delete(rev)
            mysql.session.commit()
        except Exception as e:
            print(e, file=stderr)
            return make_response({"message": "Db deletion error"}, 400)
    else:
        return make_response({"message": "Wrong review id"}, 400)

    return make_response({"message": "Success"}, 200)