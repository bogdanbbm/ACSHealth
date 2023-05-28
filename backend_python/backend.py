from flask import Flask
from flask_cors import CORS
from utils import mysql
from identity import identity_blueprint
from images import images_blueprint
from medic_data import medic_blueprint
from medical_data import medical_data_blueprint
from appointments import appointments_blueprint
from clinics import clinics_blueprint
from personal_data import patient_data_blueprint
from blood_donations import blood_donations_blueprint

app = Flask(__name__)

# config mysql database with sqlalchemy for the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://prod:something_encrypt3d@mysql-database/ip"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == '__main__':
    # init database and create all models    
    with app.app_context():
        mysql.init_app(app)
        mysql.create_all()

    # register blueprints for all modules
    app.register_blueprint(identity_blueprint)
    app.register_blueprint(images_blueprint)
    app.register_blueprint(medic_blueprint)
    app.register_blueprint(medical_data_blueprint)
    app.register_blueprint(appointments_blueprint)
    app.register_blueprint(clinics_blueprint)
    app.register_blueprint(patient_data_blueprint)
    app.register_blueprint(blood_donations_blueprint)

    # run app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)