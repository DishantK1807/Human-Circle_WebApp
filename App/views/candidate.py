from App.views.home import *


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    db = mysql.connection.cursor()
    if request.method == 'POST':
        db.execute(
            "INSERT IGNORE INTO candidates (uid, fname, lname, email, cv, pp, ans, sel) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(
                session['user_id'], request.form.get('fname'), request.form.get('lname'), request.form.get('email'),
                request.form.get('cv'), request.form.get('pp'), request.form.get('ans'), request.form.get('sel')))
        mysql.connection.commit()

        db.execute("UPDATE users SET fname='{0}', lname='{1}', email='{2}' ".format(
                    request.form.get('fname'), request.form.get('lname'), request.form.get('email')))
        mysql.connection.commit()

    else:
        db.execute("SELECT fname, lname, email FROM users WHERE id = '{}'".format(session['user_id']))
        rv = db.fetchone()
        return render_template('profile.html', fname=rv['fname'], lname=rv['lname'], email=rv['email'])


@app.route('/book', methods=['GET', 'POST'])
def book():
    db = mysql.connection.cursor()
    if request.method == 'POST':
        None
        # TODO

    else:
        if app.config['stage'] == 1:
            return render_template('failure.html', msg="This phase hasn't started yet")
        elif app.config['stage'] == 2:
            return render_template('book.html')
        else:
            return render_template('failure.html', msg="This phase has ended")