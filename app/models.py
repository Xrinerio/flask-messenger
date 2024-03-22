from app import app, db, login
from flask_login import UserMixin


app.app_context().push()


class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False)
    usermail = db.Column(db.String(60), nullable = False)
    userpass = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return '<Test %r>' % self.id


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), nullable = False)
    msg = db.Column(db.Text, nullable = False)
    room = db.Column(db.String, nullable = False)
        

class Rooms(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    users = db.Column(db.String)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable = False, unique = True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(1024))
    usermail = db.Column(db.String(64), nullable = False, unique = True)
    userpass = db.Column(db.String(64), nullable = False)
    img = db.Column(db.String(128), default = 'img/ava.jpg')
    sendedreq = db.Column(db.String, default = '')
    taketreq = db.Column(db.String, default = '')
    frendlist = db.Column(db.String, default = '')
    mail_conf = db.Column(db.Boolean, default = False)
    delete_acc = db.Column(db.Boolean, default = False)

    def is_active():
        if delete_acc:
            return False
        else:
            return True


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)