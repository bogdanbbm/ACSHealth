from utils import mysql
from sqlalchemy import LargeBinary

class login_details(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    username = mysql.Column(mysql.String(255))
    password = mysql.Column(mysql.String(255))
    is_medic = mysql.Column(mysql.String(1), default='N')
    completed_reg = mysql.Column(mysql.String(1), default='N')
    mail_check = mysql.Column(mysql.String(1), default='N')
    mail_uuid = mysql.Column(mysql.String(255), default='N')

    def __init__(self, username, password, is_medic, mail_uuid, completed_reg):
        self.username = username
        self.password = password
        self.is_medic = is_medic
        self.mail_uuid = mail_uuid
        self.completed_reg = completed_reg

class images(mysql.Model):
    id_medic = mysql.Column(mysql.Integer, primary_key=True)
    image_stamp = mysql.Column(mysql.TIMESTAMP, primary_key=True)
    photo = mysql.Column(LargeBinary(length=(2**32)-1))

    def __init__(self, id_medic, image_stamp, photo):
        self.id_medic = id_medic
        self.image_stamp = image_stamp
        self.photo = photo

class medic_details(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    fname = mysql.Column(mysql.String(255), default = " ")
    lname = mysql.Column(mysql.String(255), default = " ")
    rating = mysql.Column(mysql.Float)
    image_stamp = mysql.Column(mysql.TIMESTAMP, nullable=False)

    def __init__(self, id, fname, lname, rating, image_stamp):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.rating = rating
        self.image_stamp = image_stamp

class reviews(mysql.Model):
    id_review = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    id_medic = mysql.Column(mysql.Integer, nullable=False)
    review = mysql.Column(mysql.TEXT)
    rating = mysql.Column(mysql.Float)

    def __init__(self, id_medic, review, rating):
        self.id_medic = id_medic
        self.review = review
        self.rating = rating

class consultations(mysql.Model):
    id_consult = mysql.Column(mysql.Integer, primary_key=True, autoincrement=True)
    id_medic = mysql.Column(mysql.Integer, nullable=False)
    id_patient = mysql.Column(mysql.Integer, nullable=False)
    consult_date = mysql.Column(mysql.DATE)
    treatment = mysql.Column(mysql.TEXT)

    def __init__(self, id_medic, id_patient, consult_date, treatment):
        self.id_medic = id_medic
        self.id_patient = id_patient
        self.consult_date = consult_date
        self.treatment = treatment