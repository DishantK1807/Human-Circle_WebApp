from App.views.home import *


@app.route('/iprofile', methods=['GET', 'POST'])
def iprofile():
    '''View Interviewer Profile'''
    db = mysql.connection.cursor()
    if request.method == 'POST':
        return redirect(url_for('iedit'))
    else:
        db.execute(
            "SELECT fname, lname, email, pp FROM interviewers WHERE uid = '{}'".format(decode_auth(session['user_id'])))
        rv = db.fetchone()
        return render_template('interviewer/profile.html', user=rv)


@app.route('/iedit', methods=['GET', 'POST'])
def iedit():
    '''Edit Candidate Profile'''
    sessionid = decode_auth(session['user_id'])
    db = mysql.connection.cursor()
    if request.method == 'POST':
        rows = db.execute(
            "UPDATE interviewers SET fname = '{0}', lname = '{1}', email = '{2}', pp = '{3}' WHERE uid = '{4}'".format(
                request.form.get('fname'), request.form.get('lname'), request.form.get('email'),
                request.form.get('pp'), sessionid))
        mysql.connection.commit()

        db.execute("UPDATE users SET fname='{0}', lname='{1}', email='{2}' WHERE id = {3}".format(
            request.form.get('fname'), request.form.get('lname'), request.form.get('email'), sessionid))
        mysql.connection.commit()

    else:
        db.execute(
            "SELECT fname, lname, email, pp FROM interviewers WHERE uid = '{}'".format(sessionid))
        rv = db.fetchone()
        return render_template('interviewer/edit.html', user=rv)


def shortlist(uid, approval):
    '''Shortlist candidates based on profiles'''
    db = mysql.connection.cursor()

    if approval == "accept":
        db.execute("SELECT * FROM candidates WHERE uid = '{}'".format(uid))
        rv = db.fetchone()

        db.execute(
            "INSERT IGNORE INTO selected (uid, fname, lname, email, cv, pp) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
             rv['uid'], rv['fname'], rv['lname'], rv['email'], rv['cv'], rv['pp'] ))
        mysql.connection.commit()

        return redirect(url_for('index'))
    else:
        db.execute("DELETE FROM candidates WHERE uid = '{}'".format(uid))
        return redirect(url_for('index'))


def select(uid, approval):
    '''Select candidates after the interview'''
    db = mysql.connection.cursor()
    if approval == "accept":
        db.execute("SELECT * FROM selected WHERE uid = '{}'".format(uid))
        rv = db.fetchone()

        db.execute(
            "INSERT IGNORE INTO final (uid, fname, lname, email, cv, pp) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
             rv['uid'], rv['fname'], rv['lname'], rv['email'], rv['cv'], rv['pp'] ))
        mysql.connection.commit()
        return redirect(url_for('index'))
    else:
        db.execute("DELETE FROM selected WHERE uid = '{}'".format(uid))
        return redirect(url_for('index'))
