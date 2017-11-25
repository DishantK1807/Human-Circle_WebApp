from App.views.home import *
from App.views.login import hashpass, verify_user, register_candidate
from App.views.oauth import add_user

FACEBOOK_APP_ID = '149755659083642'
FACEBOOK_APP_SECRET = '5a21a075f8cbfd2c3a1f5b6dc5523338'
REDIRECT_URI = '/facebookcallback'


facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            request_token_url=None,
                            request_token_params={'scope': 'email'},
                            access_token_url='/oauth/access_token',
                            access_token_method='POST',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET)


@app.route('/facebookauth')
def facebookauth():
    callback=url_for('facebookcallback', _external=True, next=request.args.get('next') or request.referrer or None)
    return facebook.authorize(callback=callback)


@app.route(REDIRECT_URI)
@facebook.authorized_handler
def facebookcallback(resp):
    if resp is None:
        return render_template('failure.html', msg='No response from Facebook account')

    access_token = resp['access_token']
    session['token'] = access_token, ''
    user_data = facebook.get('/me?fields=first_name,last_name,email').data
    password = hashpass(user_data['id'])

    add_user(user_data['id'], user_data['email'], password, user_data['first_name'],  user_data['last_name'])

    # return render_template('failure.html', msg=str(user_data))
    return redirect(url_for('index'))


@facebook.tokengetter
def get_access_token(token=None):
    return session.get('token')