import hashlib
from codecs import encode
from tempfile import gettempdir

from flask import Flask, request
from flask_mysqldb import MySQL
from flask_session import Session

from App.helpers import *

app = Flask(__name__)

app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = '456123'
app.config['MYSQL_DB']          = 'yic'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR']  = gettempdir()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE']      = 'filesystem'
Session(app)


@app.route('/')
@login_required
def index():
    if session.get('auth_lvl')      == 0:
        return render_template('index_a.html')
    elif session.get('auth_lvl')    == 1:
        return render_template('index_m.html')
    elif session.get('auth_lvl')    == 2:
        return render_template('index_i.html')
    else:
        return render_template('index.html')


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
        if not request.form.get("username") or not request.form.get("password"):
            return render_template('failure.html', msg='Username/Password fields cannot be empty')
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
            db.execute("INSERT IGNORE INTO tempusers (uname, pass, authlvl) VALUES ('{0}', '{1}', '{2}')".format(
                request.form.get("username"), password, request.form.get("auth")))
            mysql.connection.commit()

        # add candidate ids to main table
        else:
            db.execute("INSERT IGNORE INTO users (uname, pass, authlvl) VALUES ('{0}', '{1}', '{2}')".format(
                request.form.get("username"), password, request.form.get("auth")))
            mysql.connection.commit()

            # get id and authlvl
            db.execute("SELECT * FROM users WHERE uname = '{}'".format(request.form.get("username")))
            rv = db.fetchone()

            # create session
            session['user_id']  = rv['id']
            session['auth_lvl'] = int(rv['authlvl'])

        return redirect(url_for('index'))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
