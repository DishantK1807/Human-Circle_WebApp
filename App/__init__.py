from tempfile import gettempdir

from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session
from flask_mail import Mail

app = Flask(__name__)

app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = '456123'
app.config['MYSQL_DB']          = 'yic'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
DEFAULT_MAIL_SENDER = 'Young India Challenge'
mail = Mail(app)

# configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR']  = gettempdir()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE']      = 'filesystem'
Session(app)

app.config['stage'] = 2

from App.helpers import *
from App.views import home
from App.views import login
from App.views import admin
from App.views import candidate
from App.views import interviewer

if __name__ == '__main__':
    app.run(debug=True)
