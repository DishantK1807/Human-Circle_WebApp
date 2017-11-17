import hashlib
from codecs import encode
from tempfile import gettempdir

from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_session import Session
from flask_mail import Message
from flask_oauthlib.client import OAuth

from App.helpers import *
from App import app
from App import mysql
from App import mail
from App import oauth

from App.views import admin
from App.views import interviewer


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Admin
    if session.get('auth_lvl')      == 0:
        if request.method == 'POST':
            return admin.add(request.form.get('email'), request.form.get("approval"))
        else:
            db = mysql.connection.cursor()
            db.execute("SELECT * FROM tempusers ORDER BY fname")
            return render_template('admin/index.html', rows=db.fetchall())

    # Mentor
    elif session.get('auth_lvl')    == 1:
        return render_template('mentor/index.html')

    # Interviewer
    elif session.get('auth_lvl')    == 2:
        if request.method == 'POST':
            if app.config['stage'] == 2:
                return interviewer.shortlist(request.form.get('uid'), request.form.get("approval"))
            elif app.config['stage'] == 3:
                return interviewer.select(request.form.get('uid'), request.form.get("approval"))
            else:
                return None

        else:
            db = mysql.connection.cursor()
            if app.config['stage'] < 2:
                return render_template('failure.html', msg="This phase hasn't started yet")

            elif app.config['stage'] == 2:
                db.execute("SELECT * FROM candidates ORDER BY fname")
                return render_template('interviewer/index.html', rows=db.fetchall())

            elif app.config['stage'] == 3:
                db.execute("SELECT * FROM selected ORDER BY fname")
                return render_template('interviewer/index.html', rows=db.fetchall())

            else:
                return render_template('failure.html', msg="This phase has ended")

    # Candidate
    else:
        db = mysql.connection.cursor()
        db.execute("SELECT * FROM candidates WHERE uid = {}".format(decode_auth(session['user_id'])))
        return render_template('candidate/index.html', user=db.fetchone())


