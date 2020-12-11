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
import sqlite3
import json
import validation

import dbController

app = Flask(__name__)

csrf = CSRFProtect()
csrf.init_app(app)
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

csrf.init_app(app)

app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 600
jwt = JWTManager(app)

HOST = 'localhost'
session_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=0)

# create DB
try:
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    with open('createScript.sql', 'r') as sqlite_file:
        sql_script = sqlite_file.read()

    cursor.executescript(sql_script)
    print("SQLite script executed successfully")
    cursor.close()

except sqlite3.Error as error:
    print("Error while executing sqlite script", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")

dbc = dbController


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
        View('My notes', 'mynotes'),
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
        dbc.insertUser(form.login.data, password, form.email.data)
        return render_template('index.html', reg=True)

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET', 'HEAD', 'OPTIONS'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = dbc.getUserByLogin(form.loginl.data)
        if user is not None:
            stored = user[2]
            if verify_password(stored, form.passwordl.data):
                login = form.loginl.data
                userid = uuid4().hex
                # name_hash = hashlib.sha512(username.encode()).hexdigest()
                # session_db.set(username, name_hash, ex=600)
                session_db.set(userid, login, ex=600)
                response = redirect(url_for('index'))
                # response.set_cookie(SESSION_ID, username, max_age=600, httponly=True)
                response.set_cookie(SESSION_ID, userid, max_age=600)
                token = create_access_token(identity=login)
                response.set_cookie("jwt", token, max_age=600)
                response.set_cookie('login', login, max_age=600)
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
    response.set_cookie(SESSION_ID, '', expires=0)
    response.set_cookie("jwt", '', expires=0)
    response.set_cookie('login', '', max_age=600)
    return response


@app.route('/notes', methods=[GET])
def notes():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    notes = dbc.getAllPublicNotes()
    print(notes)
    if notes == -1:
        return render_template('myfiles.html')
    return render_template('myfiles.html', notes=notes)


@app.route('/mynotes', methods=[GET])
def mynotes():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    user = request.cookies.get('login')
    user_data = dbc.getUserByLogin(user)
    user_id = user_data[0]
    notes = dbc.getUserNotes(user_id)
    print(notes)

    return render_template('myfiles.html', notes=notes)


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
        user = request.cookies.get('login')
        user_data = dbc.getUserByLogin(user)
        user_id = user_data[0]
        dbc.updatePassword(user_id, hash_password(form.newpassword.data))
        return render_template('changegood.html')
    return render_template('changepasswd.html', form=form)


@app.route('/note/<id>', methods=[GET, POST])
def note(id):
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    note = dbc.getNote(id)
    user_id = note[1]
    print(note)
    print(user_id)
    user = dbc.getUserById(user_id)
    print(user)
    author = user[1]
    title = note[3]
    content = note[4]
    return render_template('note.html', content=content, title=title, author=author)


@app.route('/addnote', methods=[GET, POST])
def addnote():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return redirect(url_for('logout'))
    if not session_db.exists(session_id):
        return redirect(url_for('logout'))
    form = AddNoteForm()
    if form.validate_on_submit():
        user = request.cookies.get('login')
        user_data = dbc.getUserByLogin(user)
        user_id = user_data[0]
        if form.isPrivate.data:
            isPrivate = 1
        else:
            isPrivate = 0
        dbc.insertNote(user_id, isPrivate, form.name.data, form.content.data)
        return render_template('uploadgood.html')
    return render_template('addnote.html', form=form)


@csrf.exempt
@app.route('/api/register', methods=[POST])
def api_register():
    if request.method == POST:
        response = make_response('', 400)
        data = json.loads(request.data)
        print(data)
        user = dbc.getUserByLogin(data['login'])
        if user is not None:
            response = make_response('User is already present', 400)
            return response
        login = data['login']
        passwd = data['password']
        confirm = data['confirm_password']
        email = data['email']
        response = make_response('Could not add user', 400)
        if validation.validateRegister(login, passwd, confirm, email):
            dbc.insertUser(login, hash_password(passwd), email)
            response = make_response('', 200)
    return response


@csrf.exempt
@app.route('/api/login', methods=[GET, POST])
def api_login():
    if request.method == GET:
        response = make_response('', 400)
        session_id = request.cookies.get(SESSION_ID)
        if session_id is None:
            return response
        if not session_db.exists(session_id):
            return response
        response.status_code = 200
        return response
    if request.method == POST:
        response = make_response('', 400)
        data = json.loads(request.data)
        user = dbc.getUserByLogin(data['loginl'])
        if user is not None:
            login = data['loginl']
            passwd = data['passwordl']
            if validation.validateLogin(login, passwd):
                stored = user[2]
                if verify_password(stored, data['passwordl']):
                    login = data['loginl']
                    userid = uuid4().hex
                    # name_hash = hashlib.sha512(username.encode()).hexdigest()
                    # session_db.set(username, name_hash, ex=600)
                    session_db.set(userid, login, ex=600)
                    # response.set_cookie(SESSION_ID, username, max_age=600, httponly=True)
                    response.set_cookie(SESSION_ID, userid, max_age=600)
                    token = create_access_token(identity=login)
                    response.set_cookie("jwt", token, max_age=600)
                    response.set_cookie('login', login, max_age=600)
                    response.status_code = 200
                    return response
    response = make_response('', 400)
    return response


@csrf.exempt
@app.route('/api/changepasswd', methods=[POST])
def api_changepasswd():
    return "A"


@csrf.exempt
@app.route('/api/notes', methods=[POST])
def api_notes():
    return "A"


@csrf.exempt
@app.route('/api/note/<id>', methods=[GET])
def api_note(id):
    return "A"


@csrf.exempt
@app.route('/api/addnote', methods=[POST])
def api_addnote():
    return "A"


@csrf.exempt
@app.route('/api/pnotes', methods=[GET])
def api_pnotes():
    return "A"


@csrf.exempt
@app.route('/api/logout', methods=[POST])
def api_logout():
    response = make_response('', 200)
    session_id = request.cookies.get(SESSION_ID)
    if session_id is None:
        return response
    if session_db.exists(session_id):
        session_db.delete(session_id)
        response.set_cookie(SESSION_ID, '', expires=0)
        response.set_cookie("jwt", '', expires=0)
        response.set_cookie("login", '', expires=0)
    return response


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=False)
    # app.run()
