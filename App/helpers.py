from App import app

from functools import wraps
import datetime
import jwt

from flask import redirect, session, url_for, render_template


def apology(msg=""):
    """Renders message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("failure.html", msg=escape(msg))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def encode_auth(user_id):
    """
        Generates the Auth Token
        :return: string
    """
    try:
        payload = {
            # Time of Generation of the Token
            'iat': datetime.datetime.utcnow(),
            # Subject
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth(auth_token):
    """
    Decodes the auth token
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.exceptions.InvalidTokenError:
        return 'Invalid token. Please log in again.'
