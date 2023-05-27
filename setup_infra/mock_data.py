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

# TODO: add consultations

# TODO: add clinics

# TODO: add appointments

# TODO: add blood donations
