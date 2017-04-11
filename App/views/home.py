import hashlib
from codecs import encode
from tempfile import gettempdir

from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_session import Session

from App.helpers import *
from App import app
from App import mysql

from App.views import admin


@app.route('/')
@login_required
def index():
    if session.get('auth_lvl')      == 0:
        return admin.approval(session.get('user_id'))
    elif session.get('auth_lvl')    == 1:
        return render_template('index_m.html')
    elif session.get('auth_lvl')    == 2:
        return render_template('index_i.html')
    else:
        return render_template('index.html')


