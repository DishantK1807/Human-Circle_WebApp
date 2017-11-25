from App.views.home import *
from App.views.login import hashpass, verify_user, register_candidate


def add_user(id, email, password, fname, lname):
    db = mysql.connection.cursor()
    rows = db.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    rv = db.fetchone()

    if verify_user(email, str(id)) is False:
        register_candidate(db, email, password, fname, lname, auth=int(3))
    return


GOOGLE_CLIENT_ID = '418555457379-s4qrcjttitvokgckatucvsmd2dvokt44.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'onAkS2oPYrHTBi4_l6EhLZn4'
REDIRECT_URI = '/googlecallback'


google = oauth.remote_app('google',
                          base_url='https://www.googleapis.com/oauth2/v1/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'email profile'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/googleauth')
def googleauth():
    callback=url_for('googlecallback', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def googlecallback(resp):
    if resp is None:
        return render_template('failure.html', msg='No response from Google account')
    access_token = resp['access_token']
    session['token'] = access_token, ''
    user_data = google.get('userinfo').data
    password = hashpass(user_data['id'])

    add_user(user_data['id'], user_data['email'], password, user_data['given_name'], user_data['family_name'])

    #return render_template('failure.html', msg=str(user_data))
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('token')