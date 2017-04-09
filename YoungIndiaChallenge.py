from tempfile import gettempdir

from flask import Flask, render_template, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from helpers import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:456123@localhost/yic'
db = SQLAlchemy(app)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@login_required
def index():
    if session["authlvl"] == 1:
        render_template("index_m.html")
    elif session["authlvl"] == 2:
        render_template("index_i.html")
    else:
        render_template("index_c.html")


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
        # rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        return redirect(url_for(index))

    else:
        return render_template("login.html")


@app.route('/register')
def register():
    return None


if __name__ == '__main__':
    app.run()
