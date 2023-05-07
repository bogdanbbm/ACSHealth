from flask import Flask, request, abort, make_response, jsonify
import jwt
import json
import time
from datetime import datetime, timedelta
from flask_mysqldb import MySQL
from flask_cors import CORS
from sys import stderr
# all of these are used for imports in the different modules
from email_module import compute_email
from uuid import uuid4

app = Flask(__name__)


# Configure MySQL connection
# TODO: get these from env
app.config['MYSQL_HOST'] = 'mysql-database'
app.config['MYSQL_USER'] = 'prod'
app.config['MYSQL_PASSWORD'] = 'something_encrypt3d'
app.config['MYSQL_DB'] = 'ip'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mysql = MySQL(app)
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
import medic_data
import identity
import images
import personal_data

if __name__ == '__main__':
    # TODO: when running in prod delete debug=True
    app.run(host='0.0.0.0', port=5000, debug=True)