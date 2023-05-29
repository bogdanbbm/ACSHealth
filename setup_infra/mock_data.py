import requests
from time import sleep
import os

ip = "localhost"
port = 5000
base_url = "http://{ip}:{port}".format(ip=ip, port=port)

# add medics and patients

requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "med1", "password": "da",\
                                            "isMedic": 1})
requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "med2", "password": "da",\
                                            "isMedic": 1})
requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "med3", "password": "da",\
                                            "isMedic": 1})
requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "med4", "password": "da",\
                                            "isMedic": 1})

requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "pat1", "password": "nu",\
                                            "isMedic": 0})
requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "pat2", "password": "nu",\
                                            "isMedic": 0})
requests.post("{}/register".format(base_url),
               json={"email": "razvan.berchez@gmail.com", \
                                            "username": "pat3", "password": "nu",\
                                            "isMedic": 0})

# check mail

os.system("chmod +x check_mail.sh")
os.system("./check_mail.sh")

# login all users to insert data for them

tok = open("tokens.txt", "w")

tokens = {}

tokens["med1"] = requests.post("{}/login".format(base_url),
               json={"username": "med1", "password": "da"}).json()["token"]
tok.write("med1 -> "+tokens["med1"]+'\n')
tokens["med2"] = requests.post("{}/login".format(base_url),
               json={"username": "med2", "password": "da"}).json()["token"]
tok.write("med2 -> "+tokens["med2"]+'\n')
tokens["med3"] = requests.post("{}/login".format(base_url),
               json={"username": "med3", "password": "da"}).json()["token"]
tok.write("med3 -> "+tokens["med3"]+'\n')
tokens["med4"] = requests.post("{}/login".format(base_url),
               json={"username": "med4", "password": "da"}).json()["token"]
tok.write("med4 -> "+tokens["med4"]+'\n')
tokens["pat1"] = requests.post("{}/login".format(base_url),
               json={"username": "pat1", "password": "nu"}).json()["token"]
tok.write("pat1 -> "+tokens["pat1"]+'\n')
tokens["pat2"] = requests.post("{}/login".format(base_url),
               json={"username": "pat2", "password": "nu"}).json()["token"]
tok.write("pat2 -> "+tokens["pat2"]+'\n')
tokens["pat3"] = requests.post("{}/login".format(base_url),
               json={"username": "pat3", "password": "nu"}).json()["token"]
tok.write("pat3 -> "+tokens["pat3"]+'\n')

tok.close()

stamps = open("stamps.txt", "w")

# add medic data and images

stamp = requests.post("{}/medic_list".format(base_url),
               json={"username": "med1", "firstName": "John", "lastName": "Cena"},
               headers={'Authorization':tokens["med1"]}).json()["timestamp"]
stamps.write('John Cena -> ' + stamp + '\n')
file = {'file': open('JohnCena.jpg', 'rb')}
requests.post("{base}/images/{stamp}".format(base = base_url, stamp = stamp),
              files=file)

sleep(1)
stamp = requests.post("{}/medic_list".format(base_url),
               json={"username": "med2", "firstName": "Anne", "lastName": "Hathaway"},
               headers={'Authorization':tokens["med2"]}).json()["timestamp"]
stamps.write('Anne Hathaway -> ' + stamp + '\n')
file = {'file': open('AnneHathaway.jpg', 'rb')}
requests.post("{base}/images/{stamp}".format(base = base_url, stamp = stamp),
              files=file)

sleep(1)
stamp = requests.post("{}/medic_list".format(base_url),
               json={"username": "med3", "firstName": "Jim", "lastName": "Carrey"},
               headers={'Authorization':tokens["med3"]}).json()["timestamp"]
stamps.write('Jim Carrey -> ' + stamp + '\n')
file = {'file': open('JimCarrey.jpg', 'rb')}
resp = requests.post("{base}/images/{stamp}".format(base = base_url, stamp = stamp),
              files=file)

sleep(1)
stamp = requests.post("{}/medic_list".format(base_url),
               json={"username": "med4", "firstName": "Dwayne", "lastName": "Johnson"},
               headers={'Authorization':tokens["med4"]}).json()["timestamp"]
stamps.write('Dwayne Johnson -> ' + stamp + '\n')
file = {'file': open('DwayneJohnson.jpg', 'rb')}
resp = requests.post("{base}/images/{stamp}".format(base = base_url, stamp = stamp),
              files=file)

stamps.close()

# add medic reviews

requests.post("{}/medic_reviews/med1".format(base_url), json={"review":"foarte dezamagit",
                "rating":float(1)})
requests.post("{}/medic_reviews/med1".format(base_url), json={"review":"Nu are ce cauta acolo",
                "rating":float(2)})
requests.post("{}/medic_reviews/med1".format(base_url), json={"review":"Nesimtit",
                "rating":float(2)})
requests.post("{}/medic_reviews/med2".format(base_url), json={"review":"Ok",
                "rating":float(4)})
requests.post("{}/medic_reviews/med2".format(base_url), json={"review":"Parea putin plictisita",
                "rating":float(3)})
requests.post("{}/medic_reviews/med3".format(base_url), json={"review":"De treaba",
                "rating":float(4)})
requests.post("{}/medic_reviews/med4".format(base_url), json={"review":"Super intelegator",
                "rating":float(5)})

# add patient data

requests.post("{}/patient_data".format(base_url), json={"firstName": "Mircea",
            "lastName": "Mircea", "birthdate":"1991-11-20", "sex":"M",
            "cnp":"1245638964215", "weight":float(71.55)}, 
            headers={'Authorization':tokens["pat1"]})
requests.post("{}/patient_data".format(base_url), json={"firstName": "Ginela",
            "lastName": "Marinescu", "birthdate":"1992-09-12", "sex":"F",
            "cnp":"975463864125", "height":float(1.63)}, 
            headers={'Authorization':tokens["pat2"]})
requests.post("{}/patient_data".format(base_url), json={"firstName": "Vasile",
            "lastName": "Vasile", "birthdate":"1994-06-21", "sex":"M",
            "cnp":"5268974513875", "RH":"P", "bloodGroup":"A"}, 
            headers={'Authorization':tokens["pat3"]})

requests.post("{}/patient_data/allergies".format(base_url), json={"allergy":"bees"},
              headers={'Authorization':tokens["pat3"]})
requests.post("{}/patient_data/allergies".format(base_url), json={"allergy":"nuts"},
              headers={'Authorization':tokens["pat3"]})
requests.post("{}/patient_data/allergies".format(base_url), json={"allergy":"dust"},
              headers={'Authorization':tokens["pat2"]})
requests.post("{}/patient_data/allergies".format(base_url), json={"allergy":"cats"},
              headers={'Authorization':tokens["pat1"]})

# add clinics

requests.post("{}/clinics".format(base_url), json={"clinicName":"Medlife"})
requests.post("{}/clinics".format(base_url), json={"clinicName":"Sante"})
requests.post("{}/clinics".format(base_url), json={"clinicName":"Sanador"})

# add consultations

requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat1",
            "treatment":"Azitromicina", "consultationDate":"2019-09-18"},
            headers={'Authorization':tokens["med2"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat2",
            "treatment":"Bromhexin", "consultationDate":"2017-05-21"},
            headers={'Authorization':tokens["med1"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat2",
            "treatment":"Paracetamol", "consultationDate":"2020-11-09"},
            headers={'Authorization':tokens["med1"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat1",
            "treatment":"Aspirina", "consultationDate":"2016-10-27"},
            headers={'Authorization':tokens["med3"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat1",
            "treatment":"Ceai de ghimbir", "consultationDate":"2019-02-02"},
            headers={'Authorization':tokens["med4"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat3",
            "treatment":"Un mar pe zi timp de o luna", "consultationDate":"2018-08-19"},
            headers={'Authorization':tokens["med3"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat3",
            "treatment":"Paracetamol", "consultationDate":"2020-07-13"},
            headers={'Authorization':tokens["med4"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat3",
            "treatment":"O saptamana la munte", "consultationDate":"2020-09-18"},
            headers={'Authorization':tokens["med2"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat2",
            "treatment":"Frectie cu carmol", "consultationDate":"2020-09-18"},
            headers={'Authorization':tokens["med2"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat3",
            "treatment":"Tussin Forte", "consultationDate":"2022-04-06"},
            headers={'Authorization':tokens["med1"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat1",
            "treatment":"GrinTuss", "consultationDate":"2017-07-17"},
            headers={'Authorization':tokens["med3"]})
requests.post("{}/medical_data".format(base_url), json={"patientUsername":"pat1",
            "treatment":"Colebil", "consultationDate":"2019-01-04"},
            headers={'Authorization':tokens["med4"]})

# add appointments

requests.post("{}/appointments".format(base_url), json={"clinicName":"Sante",
            "medicUsername":"med2", "appointmentDate":"2023-06-17"},
            headers={'Authorization':tokens["pat1"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Sanador",
            "medicUsername":"med1", "appointmentDate":"2023-07-06"},
            headers={'Authorization':tokens["pat1"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Sante",
            "medicUsername":"med3", "appointmentDate":"2023-06-21"},
            headers={'Authorization':tokens["pat2"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Medlife",
            "medicUsername":"med3", "appointmentDate":"2023-07-16"},
            headers={'Authorization':tokens["pat3"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Medlife",
            "medicUsername":"med4", "appointmentDate":"2023-08-09"},
            headers={'Authorization':tokens["pat2"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Sante",
            "medicUsername":"med1", "appointmentDate":"2023-06-22"},
            headers={'Authorization':tokens["pat1"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Sanador",
            "medicUsername":"med4", "appointmentDate":"2023-07-29"},
            headers={'Authorization':tokens["pat2"]})
requests.post("{}/appointments".format(base_url), json={"clinicName":"Medlife",
            "medicUsername":"med3", "appointmentDate":"2023-08-12"},
            headers={'Authorization':tokens["pat3"]})

# add blood donations

requests.post("{}/blood_donations".format(base_url), json={"patientUsername":"pat1",
            "donationDate":"2020-02-07"}, headers={'Authorization':tokens["med4"]})
requests.post("{}/blood_donations".format(base_url), json={"patientUsername":"pat1",
            "donationDate":"2019-05-19"}, headers={'Authorization':tokens["med3"]})
requests.post("{}/blood_donations".format(base_url), json={"patientUsername":"pat2",
            "donationDate":"2021-10-22"}, headers={'Authorization':tokens["med1"]})
requests.post("{}/blood_donations".format(base_url), json={"patientUsername":"pat1",
            "donationDate":"2018-09-26"}, headers={'Authorization':tokens["med4"]})
requests.post("{}/blood_donations".format(base_url), json={"patientUsername":"pat3",
            "donationDate":"2017-07-16"}, headers={'Authorization':tokens["med2"]})