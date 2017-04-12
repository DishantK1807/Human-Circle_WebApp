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

def add(username, approval):
    # create connection
    db = mysql.connection.cursor()

    if approval == "accept":
        db.execute("SELECT * FROM tempusers WHERE uname = '{}'".format(username))
        rv = db.fetchone()

        db.execute(
            "INSERT IGNORE INTO users (uname, pass, fname, lname, email, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                rv['uname'], rv['pass'], rv['fname'], rv['lname'], rv['email'], rv['authlvl']))
        mysql.connection.commit()
        db.execute("DELETE FROM tempusers WHERE uname = '{}'".format(username))
        mysql.connection.commit()
        # return render_template("failure.html", msg="Accepted")

    else:
        db.execute("DELETE FROM tempusers WHERE uname = '{}'".format(username))
        mysql.connection.commit()
        # return render_template("failure.html", msg=str(username) + "  " + str(approval))
    return redirect(url_for("index"))


