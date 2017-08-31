from App.views.home import *


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
