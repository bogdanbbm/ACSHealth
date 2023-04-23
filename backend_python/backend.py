from flask import Flask, request, abort
from flask_mysqldb import MySQL
from flask_cors import CORS
from sys import stderr
from email_module import compute_email
from uuid import uuid4

app = Flask(__name__)

# Configure MySQL connection
# TODO: get these from env
app.config['MYSQL_HOST'] = 'mysql-database'
app.config['MYSQL_USER'] = 'prod'
app.config['MYSQL_PASSWORD'] = 'something_encrypt3d'
app.config['MYSQL_DB'] = 'ip'

mysql = MySQL(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    # TODO: when running in prod delete debug=True
    app.run(host='0.0.0.0', port=5000, debug=True)