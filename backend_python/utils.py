from flask_sqlalchemy import SQLAlchemy

mysql = SQLAlchemy()

# TODO: find better way to validate json
def validate_json(list_of_fields, json):
    """
    Check if json has the right fields
    """
    for field in list_of_fields:
        if field not in json:
            return False
    return True