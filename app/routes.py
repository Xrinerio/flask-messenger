from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import join_room, leave_room, send
from werkzeug.security import check_password_hash, generate_password_hash
import random
from string import ascii_uppercase
import os
from app import app, db, socketio
from app.models import Messages, User, Rooms
from config import Config
from app.email import send_email, generate_token, confirm_token

def combine_users(id1, id2):
    a=[]
    a.append(int(id1))
    a.append(int(id2))
    a.sort()
    print(a)
    return ','.join(list(map(str,a)))

def generate_unique_code(length, table, code_type='string'):
    if code_type == 'string':
        while True:
            code = ""
            for _ in range(length):
                code += random.choice(ascii_uppercase)
            
            if table.query.filter_by(id = code).first() == None:
                break
        
        return code
    elif code_type == 'int':
        while True:
            code = ""
            for _ in range(length):
                code += random.choice('1234567890')
            
            if table.query.filter_by(id = int(code)).first() == None:
                break
        
        return int(code)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/profile/')
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return redirect('/profile/'+str(current_user.id))
    else:
        return redirect(url_for('index'))



@app.route('/profile/<string:id>/confmail', methods=('GET', 'POST'))
def con_mail(id):
    if current_user.is_authenticated:
        html = render_template('letter.html')
        subject = "Please confirm your email"
        send_email(current_user.usermail, subject, html)
    else:
        return redirect(url_for('profile'))



@app.route('/profile/<string:id>', methods=('GET', 'POST'))
def Userprofile(id):
    if current_user.is_authenticated:
        if request.method == 'POST':
            newMail = request.form['mail']
            newPas = request.form['pass']
            newImg = request.files['img']
            newName = request.form['name']
            newStat = request.form['statuss']

            usera = User.query.get(current_user.id)

            if newImg.filename != '':
                filename = str(current_user.id)+'.jpg'
                usera.img = "/usersimg/"+filename
                newImg.save(os.path.join(Config.UPLOAD_FOLDER, filename))

            if newMail != '' and newMail != current_user.usermail:
                if not User.query.filter_by(usermail=newMail).first():
                    usera.usermail = newMail

            if newPas != '' and newPas != current_user.userpass:
                usera.userpass = newPas
            
            if newName != '' and newName != current_user.name:
                usera.name = newName

            if newStat != '' and newStat != current_user.status:
                usera.status = newStat

            db.session.commit()

            return redirect(url_for('Userprofile', id = id))


        else:
            user = User.query.get(id)
            return render_template('profile.html', user=user, i=User.query.get(current_user.id))
    else:
        user = User.query.get(id)
        return render_template('profile.html', user=user)


@app.route('/about')
def about():
    if current_user.is_authenticated:
        return render_template('about.html')
    else: 
        return redirect(url_for('index'))



@app.route('/friends')
def friends():
    if current_user.is_authenticated:
        users_info = User.query.all()
        return render_template('friends.html', users_info=users_info, cu_user=User.query.get(current_user.id))
    else: 
        return redirect(url_for('index'))
    db.session.commit()



@socketio.on('add')
def add(data):
    print(type(str(123)))
    current_user_db = User.query.get(current_user.id)
    try:
        add_user_db = User.query.get(data['data'].split('_')[1])
    except:
        return

    actionid = data['data'].split('_')
    print(actionid)
    if actionid[0] == 'add':
        current_user_db.sendedreq += ',' + actionid[1]
        add_user_db.taketreq += ',' + str(current_user.id)

    elif actionid[0] == 'undo':
        cu_sendlist = current_user_db.sendedreq.split(',')
        cu_sendlist.remove(actionid[1])
        current_user_db.sendedreq = ','.join(cu_sendlist)

        addu_takelist = add_user_db.taketreq.split(',')
        addu_takelist.remove(str(current_user.id))
        add_user_db.taketreq = ','.join(addu_takelist)

    elif actionid[0] == 'del':
        cu_friendlist = current_user_db.frendlist.split(',')
        cu_friendlist.remove(actionid[1])
        current_user_db.frendlist = ','.join(cu_friendlist)

        addu_friendlist = add_user_db.frendlist.split(',')
        addu_friendlist.remove(str(current_user.id))
        add_user_db.frendlist = ','.join(addu_friendlist)

    elif actionid[0] == 'acc':
        cu_sendlist = current_user_db.taketreq.split(',')
        cu_sendlist.remove(actionid[1])
        current_user_db.taketreq = ','.join(cu_sendlist)

        addu_takelist = add_user_db.sendedreq.split(',')
        addu_takelist.remove(str(current_user.id))
        add_user_db.sendedreq = ','.join(addu_takelist)
        
        cu_friendlist = current_user_db.frendlist.split(',')
        cu_friendlist.append(actionid[1])
        current_user_db.frendlist = ','.join(cu_friendlist)

        addu_friendlist = add_user_db.frendlist.split(',')
        addu_friendlist.append(str(current_user.id))
        add_user_db.frendlist = ','.join(addu_friendlist)

    db.session.commit()


@app.route('/allusers')
def allusers():
    print('!!!!!!!!!!!!!!!!!')
    if current_user.is_authenticated:
        session['room'] = ''
        users = User.query.order_by(User.username).all()
        userinfo = User.query.get(current_user.id)
        friends = userinfo.frendlist.split(',')
        sendedreq = userinfo.sendedreq.split(',')
        taketreq = userinfo.taketreq.split(',')

        return render_template('allusers.html', users=users, friends=friends, sendedreq=sendedreq, taketreq=taketreq)
    else: 
        return redirect(url_for('index'))



@app.route('/messages/<string:id>')
def Usermessages(id):
    if current_user.is_authenticated:
        usersinchat = combine_users(id,current_user.id)
        if Rooms.query.filter_by(users = usersinchat).first() != None:
            room = Rooms.query.filter_by(users = usersinchat).first().id
            session['room'] = room
        else:
            idroom = generate_unique_code(16, Rooms)
            session['room'] = idroom
            todb = Rooms(id = idroom, users = usersinchat)
            db.session.add(todb)
            db.session.commit()

        mesdb = Messages.query.filter_by(room = session.get("room")).order_by(Messages.id.desc())
        return render_template('room.html', mesuser = User.query.get(id), mesdb = mesdb )
    else: 
        return redirect(url_for('index'))



@socketio.on("connect")
def connect(auth):
    print('COnnected')
    room = session.get("room")
    join_room(room)



@socketio.on('message')
def Message(msg):
    if msg['msg'] == '': return
    room = session.get("room")
    username = current_user.username
    data = {
        'username': username,
        'msg': msg['msg']
    }
    send(data, broadcast = True, to=room)

    message = Messages(username = username, msg = msg['msg'], room = room)
    db.session.add(message)
    db.session.commit()



@app.route('/settings')
def settings():
    if current_user.is_authenticated:
        usr = User.query.order_by(User.id).all()
        for el in usr:
            el.frendlist = el.id
            el.sendedreq = ''
            el.taketreq = ''
            db.session.commit()

        if current_user.mail_conf:
            return render_template('settings.html', conf = "YES")
        else:
            return render_template('settings.html', conf = "NO")
        
    else: 
        return redirect(url_for('index'))



@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        Username = request.form['username']
        Password = request.form['pass']

        if Username and Password:
            user = User.query.filter_by(username=Username).first()

            if user and check_password_hash(user.userpass, Password):
                login_user(user)

                return redirect(url_for('index'))
            else:
                flash('Login or password is not correct')#!!!!!!!!!!!!!!!!!!

        else:
            flash('Please fill login and password fields')

    return render_template("login.html")



@app.route('/test')
def test():
    testbd = User.query.order_by(User.id).all()

    return render_template("test.html", articles=testbd)



@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        Name = request.form['name']
        Username = request.form['username']
        Email = request.form['email']
        Pas = request.form['pass']
        hPas = generate_password_hash(Pas)

        todb = User(id=generate_unique_code(16, User, 'int'), username=Username, usermail=Email, userpass=hPas, name=Name)


        try:
            db.session.add(todb)
            db.session.commit()
            login_user(todb)
            return redirect(url_for('index'))
        except:
            print('Error')
            return redirect('/login')
    else:
        return render_template("register.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<string:id>/dell')
@login_required
def dell(id):
    if current_user.id == int(id):
        user = User.query.get(id)
        user.delete_acc = True
        logout_user()
        db.session.commit()
        

    return redirect(url_for('test'))