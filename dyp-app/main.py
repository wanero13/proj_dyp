from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm, PasswordChangeForm, AddNoteForm
from flask_nav import Nav
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_nav.elements import Navbar, View
import redis
import hashlib, binascii, os
from uuid import uuid4
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app)
Bootstrap(app)
nav = Nav(app)
app.secret_key = "super secret key"
DELETE = "DELETE"
POST = "POST"
GET = "GET"
SESSION_ID = "session-id"
SECRET_KEY = '67556B58703273357638792F423F4428472B4B6250655368566D597133743677397A244326462948404D635166546A576E5A7234753778214125442A472D4B61'
WEB = 'localhost:5000'
REST = 'localhost:8080'
SALT = 'secretingredient'

app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 600
jwt = JWTManager(app)

HOST = 'redisdyp'
session_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=0)
user_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=1)
notes_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=2)


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


@nav.navigation()
def mynavbar():
    return Navbar(
        'SUPER SECURE APP',
        View('Main page', 'index'),
        View('Sign up', 'register'),
        View('Sign in', 'login'),
    )


@nav.navigation()
def loggednavbar():
    return Navbar(
        'SUPER SECURE APP',
        View('Main page', 'index'),
        View('Notes', 'notes'),
        View('Private notes', 'pnotes'),
        View('Add note', 'addnote'),
        View('Change Password', 'changepasswd'),
        View('Logout', 'logout'),
    )


@app.route('/')
def index():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return render_template('index.html', reg=False)
    if not session_db.exists(session_id):
        return render_template('index.html', reg=False)
    name = session_db.get(session_id)
    return render_template('logged.html', name=name)


@app.route('/register', methods=[POST, GET])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        password = hash_password(form.password.data)
        user_db.hmset(form.login.data, {'password': password, 'email': form.email.data})
        return render_template('index.html', reg=True)

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET', 'HEAD', 'OPTIONS'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user_db.exists(form.loginl.data):
            stored = user_db.hget(form.loginl.data, 'password')
            if verify_password(stored, form.passwordl.data):
                username = form.loginl.data
                userid = uuid4().hex
                # name_hash = hashlib.sha512(username.encode()).hexdigest()
                # session_db.set(username, name_hash, ex=600)
                session_db.set(userid, username, ex=600)
                response = redirect(url_for('index'))
                # response.set_cookie(SESSION_ID, username, max_age=600, httponly=True)
                response.set_cookie(SESSION_ID, userid, max_age=600, httponly=True, secure=True)
                token = create_access_token(identity=username)
                response.set_cookie("jwt", token, max_age=600, httponly=True, secure=True)
                response.set_cookie('login', username,max_age=600 , httponly=True, secure=True)
                return response
            return render_template('login.html', form=form, good=True)
        return render_template('login.html', form=form, good=True)
    return render_template('login.html', form=form, good=False)


@app.route('/logout')
def logout():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('index'))
    if session_db.exists(session_id):
        session_db.delete(session_id)
    response = redirect(url_for('index'))
    response.set_cookie(SESSION_ID, '', expires=0, httponly=True, secure=True)
    response.set_cookie("jwt", '', expires=0, httponly=True, secure=True)
    response.set_cookie('login', '', max_age=600, httponly=True, secure=True)
    return response


@app.route('/notes', methods=[GET])
def notes():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    notes = notes_db.keys('*')
    print(notes)

    return render_template('myfiles.html', notes=notes)

@app.route('/pnotes', methods=[GET])
def pnotes():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    notes = notes_db.keys('*')
    print(notes)

    return render_template('pfiles.html', notes=notes)


@app.route('/changepasswd', methods=[GET, POST])
def changepasswd():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    form = PasswordChangeForm()
    hidden = request.cookies.get('login')
    if hidden is None:
        return render_template('problem.html')
    form.hidden = hidden
    if form.validate_on_submit():
        user_db.hset(hidden, 'password', hash_password(form.newpassword.data))
        return render_template('changegood.html')
    return render_template('changepasswd.html', form=form)


@app.route('/note/<name>', methods=[GET, POST])
def note(name):
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    author = notes_db.hget(name, 'author')
    content = notes_db.hget(name, 'content')
    return render_template('note.html', content=content, author=author)

@app.route('/addnote', methods=[GET, POST])
def addnote():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    form = AddNoteForm()
    author = request.cookies.get('login')
    if form.validate_on_submit():
        notes_db.hmset(form.name.data, {'author': author, 'content': form.content.data})
        return render_template('uploadgood.html')
    return render_template('addnote.html', form=form)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
    # app.run()
