from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = '192.168.1.161'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'testulescu'
app.config['MYSQL_DB'] = 'ip'

mysql = MySQL(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Message FROM Test WHERE ID = 1")
    data = cur.fetchone()[0]
    cur.close()
    
    return str(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)