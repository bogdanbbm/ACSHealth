from __main__ import app, stderr, request, mysql, validate_json, format_sql, make_response, json
from medic_data import get_login_id

@app.route('/patient_data/<username>', methods = ["GET", "POST", "DELETE"])
def personal_data(username):
    cur = mysql.connection.cursor()
    
    if request.method == "GET":
        cur.execute("SELECT * FROM PATIENT_DATA WHERE ID = {}".format(get_login_id(username)))
        response_db = cur.fetchall()
        if response_db is not None:
            personal = []
            for entry in response_db:
                """
                ID          int NOT NULL,
                SUR_NAME    varchar(255),
                LAST_NAME   varchar(255),
                CNP         varchar(20),
                BIRTHDATE   DATE,
                SEX         varchar(1),
                HEIGHT      FLOAT,
                bloodGroup      varchar(2),
                RH          varchar(2),
                """
                alergyList = []
                cur.execute("SELECT ALERGY FROM ALERGY_LIST WHERE ID = {}".format(get_login_id(username)))
                response_alergy = cur.fetchall()
                if response_alergy is not None:
                    for alergy in response_alergy:
                        alergyList.append(alergy[0])

                personal.append({"firstName": entry[1], 
                                 "lastName": entry[2], 
                                 "cnp": entry[3], 
                                 "birthday": str(entry[4]),
                                 "sex": entry[5],
                                 "height": entry[6],
                                 "bloodGroup": entry[7],
                                 "rh": entry[8],
                                 "alergyList": alergyList,
                                 })
            return make_response(json.dumps(personal), 200)
        cur.close()
        return make_response({"message": "No data found"}, 400)
    
    elif request.method == "POST":
        data_received = request.get_json()
        if not validate_json(["firstName", "lastName", "cnp", "birthday",\
                              "sex", "height", "weight",
                              "bloodGroup", "rh", "alergyList"], data_received)\
        and\
        not validate_json(["new_weight"], data_received)\
        and\
        not validate_json(["new_alergy"]):
            cur.close()
            return make_response({"message": "Invalid json"}, 400)
        if data_received["sex"] not in ["M", "F"]:
            cur.close()
            return make_response({"message": "Sex should be M or F"}, 400)
        # TODO: check date format, bloodGroup, rh, cnp, alergyList
        if not "new_weight" in data_received:
            login_id = get_login_id(username)
            if login_id == -1:
                cur.close()
                return make_response({"message": "Bad username"}, 400)
            try:
                cur.execute("""INSERT INTO PATIENT_DATA     (ID,
                                                            FIRST_NAME,
                                                            LAST_NAME,
                                                            CNP,
                                                            BIRTHDATE,
                                                            SEX,
                                                            HEIGHT,
                                                            SGROUP,
                                                            RH)
                                    VALUES ({login_id}, {firstName}, {lastName},
                                            {cnp}, {birthday}, {sex},
                                            {height}, {bloodGroup}, {rh})"""
                                .format(
                                    login_id    = login_id,
                                    firstName       = format_sql(data_received["firstName"]),
                                    lastName       = format_sql(data_received["lastName"]),
                                    cnp         = data_received["cnp"],
                                    birthday    = format_sql(data_received["birthday"]),
                                    sex         = format_sql(data_received["sex"]),
                                    height      = data_received["height"],
                                    bloodGroup      = format_sql(data_received["bloodGroup"]),
                                    rh          = format_sql(data_received["rh"])
                                ))
            except Exception as e:
                print(e, file=stderr)
                cur.close()
                return make_response({"message": "Database insertion error"}, 500)
            mysql.connection.commit()
        # we have to insert the weight anyway
        try:
            cur.execute("""INSERT INTO WEIGHT_HISTORY   (ID,
                                                        WEIGHT_VALUE)
                                VALUES ({login_id}, {weight_value})"""
                            .format(
                                login_id        = login_id,
                                weight_value    = data_received["weight"] if "weight" in data_received\
                                else data_received["new_weight"]
                            ))
        except Exception as e:
            cur.close()
            print(e, file=stderr)
            return make_response({"message": "Database insertion error"}, 500)
        mysql.connection.commit()
        try:
            if "alergyList" in data_received:
                for alergy in data_received["alergyList"]:
                    cur.execute("""INSERT INTO ALERGY_LIST     (ID,
                                                        ALERGY)
                                VALUES ({login_id}, {alergy})"""
                            .format(
                                login_id        = login_id,
                                alergy          = format_sql(alergy)
                            ))
                    mysql.connection.commit()
            elif "new_alergy" in data_received:
                cur.execute("""INSERT INTO ALLERGY_LIST     (ID,
                                                        ALERGY)
                                VALUES ({login_id}, {alergy})"""
                            .format(
                                login_id        = login_id,
                                alergy          = data_received["new_alergy"]
                            ))
                mysql.connection.commit()
        except Exception as e:
            print(e, file=stderr)
            cur.close()
            return make_response({"message": "Database insertion error"}, 500)
        cur.close()
        return make_response({"message": "Success"}, 201)

    elif request.method == "DELETE":
        pass
    return ""
