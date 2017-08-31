from App.views.home import *


def add(email, approval):
    '''Approve Mentors and Interviewers'''
    # create connection
    db = mysql.connection.cursor()

    if approval == "accept":
        db.execute("SELECT * FROM tempusers WHERE email = '{}'".format(email))
        rv = db.fetchone()

        db.execute(
            "INSERT IGNORE INTO users (email, pass, fname, lname, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
                rv['email'], rv['pass'], rv['fname'], rv['lname'], rv['authlvl']))
        mysql.connection.commit()
        db.execute("DELETE FROM tempusers WHERE email = '{}'".format(email))
        mysql.connection.commit()
        # return render_template("failure.html", msg="Accepted")

    else:
        db.execute("DELETE FROM tempusers WHERE email = '{}'".format(email))
        mysql.connection.commit()
        # return render_template("failure.html", msg=str(username) + "  " + str(approval))
    return redirect(url_for("index"))


@app.route('/phase', methods=['GET', 'POST'])
def startphase():
    '''Start Phase'''
    if request.method == 'POST':
        if request.form.get('phase') in range(7):
            app.config['stage'] = int(request.form.get('phase'))
            return redirect(url_for('index'))
        else:
            return render_template('failure.html', msg="No such phase exist")

    else:
        return render_template('admin/phase.html')


@app.route('/mail', methods=['GET', 'POST'])
def sendmail():
    '''Send Mail'''
    if request.method == 'POST':
        db = mysql.connection.cursor()

        if app.config['stage'] >= 4:
            db.execute("SELECT fname, email FROM final")
            users = db.fetchall()
        elif app.config['stage'] >= 2:
            db.execute("SELECT fname, email FROM selected")
            users = db.fetchall()
        else:
            db.execute("SELECT fname, email FROM candidates")
            users = db.fetchall()

        subject = request.form.get('subject')
        message = request.form.get('message')
        with mail.connect() as conn:
            for user in users:
                msg = Message(recipients = user['email'],
                              body=message,
                              subject = subject)
                conn.send(msg)

    else:
        return render_template('admin/mail.html')
