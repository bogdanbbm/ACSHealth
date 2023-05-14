from __main__ import app, stderr, request, mysql, validate_json, format_sql, make_response, json, datetime
from medic_data import get_login_id

@app.route("/medical_data/<patient_username>", methods = ["GET"])
def get_medical_data(patient_username):
    cur = mysql.connection.cursor()
    login_id = get_login_id(patient_username)
    if login_id == -1:
        cur.close()
        return make_response({"message": "Bad username"}, 400)
    cur.execute("""SELECT ID_MEDIC, ID_PATIENT, CONSULTATION, TREATMENT
                    FROM CONSULTATION_LIST WHERE ID_PATIENT = {}"""
                .format(login_id))
    consultations = cur.fetchall()
    if consultations == ():
        return make_response({"message": "No consultations found"}, 200)
    cons_list = []
    for cons in consultations:
        cur.execute("""SELECT SNAME, LNAME FROM MEDIC_DETAILS WHERE ID = {}""".format(cons[0]))
        medic_name = cur.fetchone()
        if medic_name is None:
            cur.close()
            return make_response({"message": "Medic has not completed personal data"}, 400)
        cons_list.append({"medic": medic_name[0]+" "+medic_name[1],
                          "date":str(cons[2]), "treatment":cons[3]})
    return make_response(json.dumps(cons_list), 200)

@app.route("/medical_data/<medic_username>", methods = ["POST"])
def post_medical_data(medic_username):
    cur = mysql.connection.cursor()
    data_received = request.get_json()
    if not validate_json(["patient_username", "treatment", "consultation_date"],
                            data_received):
        cur.close()
    login_id = get_login_id(medic_username)
    if login_id == -1:
        cur.close()
        return make_response({"message": "Bad username"}, 400)
    
    patient_id = get_login_id(data_received["patient_username"])
    if patient_id == -1:
        cur.close()
        return make_response({"message": "Bad request"}, 400)
    
    cur.execute("""SELECT IS_MEDIC
                    FROM LOGIN_DETAILS
                    WHERE USERNAME = {}""".format(format_sql(medic_username)))
    is_medic = cur.fetchone()
    if is_medic is not None and is_medic == 'N':
        return make_response({"message": "Permission denied"}, 403)
    try:
        date = datetime.strptime(data_received["consultation_date"], "%d/%m/%Y")
        cur.execute("""INSERT
                    INTO CONSULTATION_LIST (ID_MEDIC, ID_PATIENT, CONSULTATION,
                    TREATMENT) VALUES ({med_id}, {pat_id}, {cons_date}, {treat})"""
                    .format(med_id = login_id,
                            pat_id = patient_id,
                            cons_date = format_sql(date.strftime('%Y-%m-%d %H:%M:%S')),
                            treat = format_sql(data_received["treatment"])))
        mysql.connection.commit()
        cur.close()
        return make_response({"message": "Consultation added successfully"}, 201)
    except Exception as e:
        print(e, file=stderr)
        cur.close()
        return make_response({"message": "Database insertion error"}, 500)

@app.route("/medical_data/<username>", methods = ["DELETE"])
def delete_medical_data(username):
    pass