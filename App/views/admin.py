from App.views.home import *

def add(username, approval):
    # create connection
    db = mysql.connection.cursor()

    if approval == "accept":
        db.execute("SELECT * FROM tempusers WHERE uname = '{}'".format(username))
        rv = db.fetchone()

        db.execute(
            "INSERT IGNORE INTO users (uname, pass, fname, lname, email, authlvl) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                rv['uname'], rv['pass'], rv['fname'], rv['lname'], rv['email'], rv['authlvl']))
        mysql.connection.commit()
        db.execute("DELETE FROM tempusers WHERE uname = '{}'".format(username))
        mysql.connection.commit()
        # return render_template("failure.html", msg="Accepted")

    else:
        db.execute("DELETE FROM tempusers WHERE uname = '{}'".format(username))
        mysql.connection.commit()
        # return render_template("failure.html", msg=str(username) + "  " + str(approval))
    return redirect(url_for("index"))


@app.route('/phase', methods=['GET', 'POST'])
def startphase():
    if request.method == 'POST':
        if request.form.get('phase') in range(7):
            app.config['stage'] = int(request.form.get('phase'))
            return redirect(url_for('index'))
        else:
            return render_template('failure.html', msg="No such phase exist")

    else:
        return render_template('phase.html')
