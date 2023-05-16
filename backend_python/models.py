from utils import mysql

# TODO: create all database models (follow dbsetup.sql for a guideline)

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