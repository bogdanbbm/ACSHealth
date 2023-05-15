from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# all of these are used for imports in the different modules

app = Flask(__name__)


# Configure MySQL connection
# TODO: get these from env
# app.config['MYSQL_HOST'] = 'mysql-database'
# app.config['MYSQL_USER'] = 'prod'
# app.config['MYSQL_PASSWORD'] = 'something_encrypt3d'
# app.config['MYSQL_DB'] = 'ip'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://prod:something_encrypt3d@mysql-database/ip"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def format_sql(command):
    """
    This just helps with strings in sql commands
    """
    return "\'" + command + "\'"
 
def validate_json(list_of_fields, json):
    """
    Check if json has the right fields
    """
    for field in list_of_fields:
        if field not in json:
            return False
    return True

# import all modules
# import medical_data
# import medic_data
# import images
# import personal_data

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

if __name__ == '__main__':
    # TODO: when running in prod delete debug=True
    with app.app_context():
        mysql.create_all()
    from identity import identity_blueprint
    app.register_blueprint(identity_blueprint)
    app.run(host='0.0.0.0', port=5000, debug=True)