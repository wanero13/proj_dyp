from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, Email, EqualTo, ValidationError
import redis
import hashlib, binascii

HOST = 'redisdyp'
session_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=0)
user_db = redis.Redis(host=HOST, port=6379, decode_responses=True, db=1)

class RegisterForm(FlaskForm):
    login = StringField('Login', validators=[InputRequired(), Length(min=4, max=24, message='Login ust be between 4 and 24 characters'), Regexp('^[A-Za-z0-9]{4,24}', message='Login can have only Letters and numbers')])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8, max=16, message='Password must have between 8 and 16 characters'), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])
    confirm = PasswordField('Confirm password', validators=[InputRequired(), Length(min=8, max=16), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])
    email = StringField('Email', validators=[InputRequired(), Email(message='This must follow standard email pattern!'), Length(min=4, max=50, message='This site doesnt accept emails longer than 50 characters(or shorter than 4)')])
    def validate_login(form, field):
        if user_db.exists(field.data):
            raise ValidationError('This login is already taken!')


class LoginForm(FlaskForm):
    loginl = StringField('Login', validators=[InputRequired(), Length(min=4, max=24, message='Login ust be between 4 and 24 characters'), Regexp('^[A-Za-z0-9]{4,24}', message='Login can have only Letters and numbers')])
    passwordl = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=16, message='Password must have between 8 and 16 characters'), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])

    def validate_loginl(form,field):
        if not user_db.exists(field.data):
            raise ValidationError('This login does not exist!')

    def validate_passwordl(form, field):
        if user_db.exists(form.loginl.data):
            password = user_db.hget(form.loginl.data, 'password')
            if not verify_password(password, field.data):
                raise ValidationError('Wrong password!')


class PasswordChangeForm(FlaskForm):
    hidden = HiddenField('hidden')
    oldpassword = PasswordField('Old Password', validators=[InputRequired(), Length(min=8, max=16, message='Password must have between 8 and 16 characters'), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])
    newpassword = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=16, message='Password must have between 8 and 16 characters'), EqualTo('confirm', message='Passwords must match'), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])
    confirm = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=16, message='Password must have between 8 and 16 characters'), Regexp('.*[0-9].*', message='Password must contain at least one digit'), Regexp('.*[A-Z].*', message='Password must contain at least one capital letter'), Regexp('.*[!@#$%^&*()].*', message='Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]'), Regexp('^[a-zA-Z0-9!@#$%^&*()]{8,16}', message='Password can have letters numbers and special signs(ones above numbers)')])

    def validate_newpassword(form, field):
        if field.data == form.oldpassword.data:
            raise ValidationError('Your new password cannot be the same as the old one!')

    def validate_oldpassword(form, field):
        old = user_db.hget(form.hidden, 'password')
        print(old)
        if not verify_password(old, field.data):
            raise ValidationError('Your new password cannot be the same as the old one!')

class AddNoteForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=3, max=20, message='Note name must be between 3 and 20 characters'), Regexp('^[a-zA-Z0-9,.!?]+', message='Name of your note must contain only letters, numbers and punctuation marks!')])
    content = TextAreaField('content', validators=[InputRequired(), Length(min=1,max=300, message='Your note must be between 1 and 300 symbols'), Regexp('^[a-zA-Z0-9,.!?]+', message='Your note can contain only letters numbers and puctuation marks!')])


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password