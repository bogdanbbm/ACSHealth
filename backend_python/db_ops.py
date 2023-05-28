from models import login_details, clinics

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

def get_clinic_name(id):
    clinic = clinics.query.filter_by(id_clinic=id).first()
    if clinic is not None:
        return clinic.name_clinic
    return ""

def get_clinic_id(clinic_name):
    clinic = clinics.query.filter_by(name_clinic=clinic_name).first()
    if clinic is not None:
        return clinic.id_clinic
    return -1