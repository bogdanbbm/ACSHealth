from utils import mysql
from models import login_details

def get_login_id(username):
    user= login_details.query.filter_by(username=username).first()
    if user is not None:
        return user.id
    return -1

def get_username(id):
    user = login_details.query.filter_by(id=id).first()
    if user is not None:
        return user.username
    return ""