import hashlib
from codecs import encode
from tempfile import gettempdir

from flask import Flask, request
from flask_mysqldb import MySQL
from flask_session import Session

from helpers import *

app = Flask(__name__)

app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = '456123'
app.config['MYSQL_DB']          = 'yic'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"]  = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]      = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    if session["auth_lvl"]    == 0:
        render_template("index_a.html")
    elif session["auth_lvl"]  == 1:
        render_template("index_m.html")
    elif session["auth_lvl"]  == 2:
        render_template("index_i.html")
    else:
        render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log User In"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
        if not request.form.get("username") or not request.form.get("password"):
            render_template("failure.html", msg="Username/Password fields cannot be empty")

        # query database for username
        db = mysql.connection.cursor()
        rows = db.execute("SELECT * FROM users WHERE uname = '{}'".format(request.form.get("username")))
        rv = db.fetchone()
        if rows or rv["pass"] == encode(hashlib.sha1(encode(request.form.get("password", 'utf-8'))).digest(),
                                        'hex_codec').decode('utf-8'):
            session["user_id"]  = rv["id"]
            session["auth_lvl"] = int(rv["authlvl"])
            return redirect(url_for("index"))
        else:
            return render_template("failure.html", msg="Invalid Username And/Or Password")

    else:
        return render_template("login.html")


@app.route('/register')
def register():
    return None


if __name__ == '__main__':
    app.run(debug=True)
