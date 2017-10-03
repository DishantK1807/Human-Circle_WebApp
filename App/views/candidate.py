from App.views.home import *


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    '''View Candidate Profile'''
    db = mysql.connection.cursor()
    if request.method == 'POST':
        return redirect(url_for('edit'))
    else:
        db.execute("SELECT fname, lname, email, cv, pp, ans FROM candidates WHERE uid = '{}'".format(decode_auth(session['user_id'])))
        rv = db.fetchone()
        return render_template('candidate/profile.html', user=rv)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    '''Edit Candidate Profile'''
    sessionid = session['user_id']
    db = mysql.connection.cursor()
    if request.method == 'POST':
        rows = db.execute(
            "UPDATE candidates SET fname = '{0}', lname = '{1}', email = '{2}', cv = '{3}', pp = '{4}', ans = '{5}', sel = '{6}' WHERE uid = '{7}'".format(
                request.form.get('fname'), request.form.get('lname'), request.form.get('email'), request.form.get('cv'),
                request.form.get('pp'), request.form.get('ans'), request.form.get('sel'), sessionid))
        mysql.connection.commit()

        db.execute("UPDATE users SET fname='{0}', lname='{1}', email='{2}' WHERE id = {3}".format(
            request.form.get('fname'), request.form.get('lname'), request.form.get('email'), sessionid))
        mysql.connection.commit()

        if rows == 0:
            return render_template('candidate/reject.html')

    else:
        db.execute(
            "SELECT fname, lname, email, cv, pp, ans FROM candidates WHERE uid = '{}'".format(sessionid))
        rv = db.fetchone()
        return render_template('candidate/edit.html', user=rv)

@app.route('/book', methods=['GET', 'POST'])
def book():
    '''Schedule Dates'''
    db = mysql.connection.cursor()

    if app.config['stage'] < 3:
        return render_template('failure.html', msg="This phase hasn't started yet")

    elif app.config['stage'] == 3:
        rows = db.execute("SELECT * FROM selected WHERE uid = '{0}'".format(decode_auth(session['user_id'])))
        if rows:
            if request.method == 'POST':
                return None
                #  TODO
            else:
                return render_template('candidate/book.html')
        else:
            return render_template('candidate/reject.html')

    else:
        return render_template('failure.html', msg="This phase has ended")


@app.route('/final', methods=['GET'])
def congrats():
    '''Final page for selected students'''
    db = mysql.connection.cursor()
    rows = db.execute("SELECT * FROM final WHERE uid = '{0}'".format(decode_auth(session['user_id'])))
    if rows:
        if app.config['stage'] < 4:
            return render_template('failure.html', msg="This phase hasn't started yet")

        elif app.config['stage'] == 4:
            return render_template('candidate/congrats.html')

        else:
            return render_template('failure.html', msg="This phase has ended")
    else:
        return render_template('candidate/reject.html')