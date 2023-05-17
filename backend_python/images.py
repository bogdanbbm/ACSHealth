from flask import Blueprint, make_response, request
from utils import mysql
from sys import stderr
from models import images, medic_details

images_blueprint = Blueprint('images', __name__)

@images_blueprint.route("/images/<timestamp>", methods = ["GET"])
def get_image(timestamp :str):
    # format timestamp
    timestamp = timestamp.replace("+", " ")

    # query database for image
    image = None
    try:
        image = images.query.filter_by(image_stamp=timestamp)
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Db selection error"}, 500)
    
    # if image exists, return it
    if image is not None:
        return make_response(image, 200)
    return make_response({"message": "Bad timestamp"}, 400)

@images_blueprint.route("/images/<timestamp>", methods = ["POST"])
def post_images(timestamp):
    # format timestamp
    timestamp = timestamp.replace("+", " ")

    # check if file has been provided
    if 'file' not in request.files:
            return make_response({"message": "No file provided"}, 400)
    
    # query database for the corresponding medic
    medic = medic_details.query().filter_by(image_stamp=timestamp).first()
    medic_id = -1
    if medic is not None:
        medic_id = medic.id
    # if medic does not exist, don't upload photo
    if medic_id == -1:
        return make_response({"message": "Invalid timestamp"}, 400)
    
    # check if filename is empty
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        query_args = (medic_id, timestamp, uploaded_file.read())
    else:
        return make_response({"message": "No filename provided"}, 400)

    # create image object and insert it into database
    try:
        image = images(query_args[0], query_args[1], query_args[2])
        mysql.session.add(image)
        mysql.session.commit()
    except Exception as e:
        print(e, file=stderr)
        return make_response({"message": "Db insertion error"}, 500)
    return make_response({"message": "Image uploaded successfully"}, 201)