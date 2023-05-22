import requests
from time import sleep

ip = "localhost"
port = 5000

# add medics
requests.post("http://{ip}:{port}/register".format(ip = ip, port = port),
               json={"email": "ciubotaruion195@gmail.com", \
                                            "username": "ceva1", "password": "da",\
                                            "isMedic": 1})
requests.post("http://{ip}:{port}/register".format(ip = ip, port = port),
               json={"email": "ciubotaruion195@gmail.com", \
                                            "username": "ceva2", "password": "da",\
                                            "isMedic": 1})
requests.post("http://{ip}:{port}/register".format(ip = ip, port = port),
               json={"email": "ciubotaruion195@gmail.com", \
                                            "username": "ceva3", "password": "da",\
                                            "isMedic": 1})

# add medic data and images
stamp = requests.post("http://{ip}:{port}/medic_list".format(ip = ip, port = port),
               json={"username": "ceva1", "firstName": "da", "lastName": "nu"}).json()["timestamp"]
file = {'file': open('absolut banal.jpg', 'rb')}
print(stamp)
requests.post("http://{ip}:{port}/images/{stamp}".format(ip = ip, port = port, stamp = stamp),
              files=file)

sleep(1)
stamp = requests.post("http://{ip}:{port}/medic_list".format(ip = ip, port = port),
               json={"username": "ceva2", "firstName": "da", "lastName": "nu"}).json()["timestamp"]
file = {'file': open('john.jpg', 'rb')}
requests.post("http://{ip}:{port}/images/{stamp}".format(ip = ip, port = port, stamp = stamp),
              files=file)

sleep(1)
stamp = requests.post("http://{ip}:{port}/medic_list".format(ip = ip, port = port),
               json={"username": "ceva3", "firstName": "da", "lastName": "nu"}).json()["timestamp"]
file = {'file': open('john2.png', 'rb')}
resp = requests.post("http://{ip}:{port}/images/{stamp}".format(ip = ip, port = port, stamp = stamp),
              files=file)
