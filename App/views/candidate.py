from App.views.home import *


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    db = mysql.connection.cursor()
    if request.method == 'POST':
        rows = db.execute(
            "UPDATE candidates SET fname = '{0}', lname = '{1}', email = '{2}', cv = '{3}', pp = '{4}', ans = '{5}', sel = '{6}' WHERE uid = '{7}'".format(
                request.form.get('fname'), request.form.get('lname'), request.form.get('email'), request.form.get('cv'),
                request.form.get('pp'), request.form.get('ans'), request.form.get('sel'), session['user_id']))
        mysql.connection.commit()

        db.execute("UPDATE users SET fname='{0}', lname='{1}', email='{2}' WHERE id = {3}}".format(
                request.form.get('fname'), request.form.get('lname'), request.form.get('email'), session['user_id']))
        mysql.connection.commit()

        if rows == 0:
            return render_template('reject.html')

    else:
        db.execute("SELECT fname, lname, email FROM users WHERE id = '{}'".format(session['user_id']))
        rv = db.fetchone()
        return render_template('profile.html', fname=rv['fname'], lname=rv['lname'], email=rv['email'])


@app.route('/book', methods=['GET', 'POST'])
def book():
    db = mysql.connection.cursor()

    if app.config['stage'] < 3:
        return render_template('failure.html', msg="This phase hasn't started yet")

    elif app.config['stage'] == 3:
        rows = db.execute("SELECT * FROM selected WHERE uid = '{0}'".format(session['user_id']))
        if rows:
            if request.method == 'POST':
                return None
                #  TODO
            else:
                return render_template('book.html')
        else:
            return render_template('reject.html')

    else:
        return render_template('failure.html', msg="This phase has ended")


@app.route('/final', methods=['GET'])
def congrats():
    db = mysql.connection.cursor()
    rows = db.execute("SELECT * FROM final WHERE uid = '{0}'".format(session['user_id']))
    if rows:
        if app.config['stage'] < 4:
            return render_template('failure.html', msg="This phase hasn't started yet")

        elif app.config['stage'] == 4:
            return render_template('congrats.html')

        else:
            return render_template('failure.html', msg="This phase has ended")
    else:
        return render_template('reject.html')