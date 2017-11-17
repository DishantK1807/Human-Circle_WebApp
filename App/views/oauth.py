from App.views.home import *


GOOGLE_CLIENT_ID = '418555457379-s4qrcjttitvokgckatucvsmd2dvokt44.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'onAkS2oPYrHTBi4_l6EhLZn4'
REDIRECT_URI = '/oauth2callback'


google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/googleauth')
def googleauth():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['user_id'] = access_token, ''
    return render_template('failure.html', msg=str(resp))


@google.tokengetter
def get_access_token():
    return session.get('user_id')