from flask import Flask
from flask_cors import CORS
from utils import mysql
# TODO: import blueprints for all modules
from identity import identity_blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://prod:something_encrypt3d@mysql-database/ip"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    # TODO: when running in prod delete debug=True
    with app.app_context():
        mysql.init_app(app)
        mysql.create_all()

    # TODO: register blueprints for all modules
    app.register_blueprint(identity_blueprint)
    app.run(host='0.0.0.0', port=5000, debug=True)