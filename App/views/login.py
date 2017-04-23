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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log User In"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
        if not request.form.get("username") or not request.form.get("password"):
            return render_template('failure.html', msg='Username/Password fields cannot be empty')

        # query database for username
        db = mysql.connection.cursor()
        rows = db.execute("SELECT * FROM users WHERE uname = '{}'".format(request.form.get("username")))
        rv = db.fetchone()

        # verify password
        if rows or rv['pass'] == encode(hashlib.sha1(encode(request.form.get("password", 'utf-8'))).digest(),
                                        'hex_codec').decode('utf-8'):
            # create session
            session['user_id']  = rv['id']
            session['auth_lvl'] = int(rv['authlvl'])
            return redirect(url_for('index'))

        else:
            return render_template('failure.html', msg="Invalid Username And/Or Password")

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
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("email"):
            return render_template('failure.html', msg='Username/ Password/ Email fields cannot be empty')
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template('failure.html', msg='Password fields do not match')

        # create connection
        db = mysql.connection.cursor()

        # query database to see if username already exists
        rows = db.execute(
            "SELECT * FROM users WHERE uname = '{0}' UNION SELECT * FROM tempusers WHERE uname = '{1}'".format(
                request.form.get("username"), request.form.get("username")))
        if rows:
            return render_template('failure.html', msg='Username Already Exists')

        # hash password with SHA-1 algorithm and store it as string
        password = encode(hashlib.sha1(encode(request.form.get("password", 'utf-8'))).digest(),
                          'hex_codec').decode('utf-8')

        # add mentor and interviewer ids to temp table for approval
        if int(request.form.get("auth")) in {0, 1, 2}:
            db.execute(
                "INSERT IGNORE INTO tempusers (uname, pass, fname, lname, email, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                    request.form.get("username"), password, request.form.get("fname"), request.form.get("lname"),
                    request.form.get("email"), request.form.get("auth")))
            mysql.connection.commit()

        # add candidate ids to main table
        else:
            db.execute(
                "INSERT IGNORE INTO users (uname, pass, fname, lname, email, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                    request.form.get("username"), password, request.form.get("fname"), request.form.get("lname"),
                    request.form.get("email"), request.form.get("auth")))
            mysql.connection.commit()

            # get id and authlvl
            db.execute("SELECT * FROM users WHERE uname = '{}'".format(request.form.get("username")))
            rv = db.fetchone()

            db.execute(
                "INSERT IGNORE INTO candidates (uid, fname, lname, email) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
                    rv['id'], request.form.get("fname"), request.form.get("lname"), request.form.get("email")
                ))
            mysql.connection.commit()

            # create session
            session['user_id']  = rv['id']
            session['auth_lvl'] = int(rv['authlvl'])

        return redirect(url_for('index'))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html')
