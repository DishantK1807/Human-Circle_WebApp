# import hashlib
# from codecs import encode
# from tempfile import gettempdir
#
# from flask import Flask, request, render_template
# from flask_mysqldb import MySQL
# from flask_session import Session
#
# from App.helpers import *
# from App import app
# from App import mysql

from App.views.home import *


def hashpass(password):
    return encode(hashlib.sha1(encode(password)).digest(), 'hex_codec').decode('utf-8')


def verify_user(email, password):
    # query database for email
    db = mysql.connection.cursor()
    rows = db.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    rv = db.fetchone()

    if not rows:
        return False

    # verify password
    if rv['pass'] == hashpass(password):
        # create session
        session['user_id'] = encode_auth(rv['id'])
        session['auth_lvl'] = int(rv['authlvl'])
        return True
    else:
        return False


def register_candidate(db, email, password, fname, lname, auth):
    db.execute(
        "INSERT IGNORE INTO users (email, pass, fname, lname, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
            email, password, fname, lname, auth))
    mysql.connection.commit()

    # get id and authlvl
    db.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    rv = db.fetchone()

    db.execute(
        "INSERT IGNORE INTO candidates (uid, fname, lname, email) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
            rv['id'], fname, lname, email))
    mysql.connection.commit()

    # create session
    session['user_id'] = encode_auth(rv['id'])
    session['auth_lvl'] = int(rv['authlvl'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log User In"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
        if not request.form.get("email") or not request.form.get("password"):
            return render_template('failure.html', msg='Email/Password fields cannot be empty')

        if verify_user(request.form.get("email"), request.form.get("password", 'utf-8')) is True:
            return redirect(url_for('index'))
        else:
            return render_template('failure.html', msg="Invalid Email And/Or Password")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register User"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # check if form fields are empty and if entered passwords match
        if not request.form.get("email") or not request.form.get("password"):
            return render_template('failure.html', msg='Email/ Password fields cannot be empty')
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template('failure.html', msg='Password fields do not match')

        # create connection
        db = mysql.connection.cursor()

        # query database to see if email already exists
        rows = db.execute(
            "SELECT * FROM users WHERE email = '{0}' UNION SELECT * FROM tempusers WHERE email = '{1}'".format(
                request.form.get("email"), request.form.get("email")))
        if rows:
            return render_template('failure.html', msg='Email Already Exists')

        # hash password with SHA-1 algorithm and store it as string
        password = hashpass(request.form.get("password", 'utf-8'))


        # add mentor and interviewer ids to temp table for approval
        if int(request.form.get("auth")) in {0, 1, 2}:
            db.execute(
                "INSERT IGNORE INTO tempusers (email, pass, fname, lname, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
                    request.form.get("email"), password, request.form.get("fname"), request.form.get("lname"),
                    request.form.get("auth")))
            mysql.connection.commit()

        # add candidate ids to main table
        else:
            register_candidate(db, request.form.get("email"),password, request.form.get("fname"),
                               request.form.get("lname"), request.form.get("auth"))

        return redirect(url_for('index'))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html')


@app.route('/developers', methods=['GET', 'POST'])
def developers():
    return render_template('dev.html')
