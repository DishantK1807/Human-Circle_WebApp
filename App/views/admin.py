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

def approval(id):
    if request.method == 'POST':

        return render_template('failure.html', msg="Index Post Request")

    else:
        return render_template('index_a.html')
