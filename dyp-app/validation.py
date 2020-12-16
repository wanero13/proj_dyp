import re
import hashlib, binascii
import dbController

dbc = dbController

def validateRegister(login, passwd, confirm, email):
    error = ''
    if not bool(re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):
        error = error + 'Email must compel to standard email pattern\n'
    if len(login) < 4 or len(login) > 24:
        error = error + 'Title must be between 3 and 20 characters\n'
    if len(passwd) < 8 or len(passwd) > 30:
        error = error + 'Content of note must be between 3 and 300 characters\n'
    if passwd != confirm:
        error = error + 'Password and its confirmation must be the same\n'
    if not bool(re.match('^[A-Za-z0-9]{4,24}', login)):
        error = error + 'Login can have only Letters and numbers!\n'
    if not bool(re.match('.*[0-9].*', passwd)):
        error = error + 'Password must contain at least one digit!\n'
    if not bool(re.match('.*[A-Z].*', passwd)):
        error = error + 'Password must contain at least one capital letter!\n'
    if not bool(re.match('.*[!@#$%^&*()].*', passwd)):
        error = error + 'Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]!\n'
    if not bool(re.match('^[a-zA-Z0-9!@#$%^&*()]{8,16}', passwd)):
        error = error + 'Password can have letters numbers and special characters!\n'
    user = dbc.getUserByLogin(login)
    if user is not None:
        error = error + 'This login is already taken!\n'

    return error


def validateLogin(login, passwd):
    error = ''
    if len(login) < 4 or len(login) > 24:
        error = error + 'Title must be between 3 and 20 characters\n'
    if len(passwd) < 8 or len(passwd) > 30:
        error = error + 'Content of note must be between 3 and 300 characters\n'
    if not bool(re.match('^[A-Za-z0-9]{4,24}', login)):
        error = error + 'Login can have only Letters and numbers!\n'
    if not bool(re.match('.*[0-9].*', passwd)):
        error = error + 'Password must contain at least one digit!\n'
    if not bool(re.match('.*[A-Z].*', passwd)):
        error = error + 'Password must contain at least one capital letter!\n'
    if not bool(re.match('.*[!@#$%^&*()].*', passwd)):
        error = error + 'Password must contain special character[ !, @, #, $, %, ^, &, *, (, ) ]!\n'
    if not bool(re.match('^[a-zA-Z0-9!@#$%^&*()]{8,16}', passwd)):
        error = error + 'Password can have letters numbers and special characters!\n'

    user = dbc.getUserByLogin(login)
    if user is None:
        error = error + 'This login does not exist!\n'
    password = user[2]
    if not verify_password(password, passwd):
        error = error + 'Wrong password!\n'

    return error


def validateNote(title, content):
    error = ''
    if len(title) < 3 or len(title) > 20:
        error = error + 'Title must be between 3 and 20 characters\n'
    if len(content) < 3 or len(content) > 300:
        error = error + 'Content of note must be between 3 and 300 characters\n'
    if not bool(re.match('^[a-zA-Z0-9,.!?]+', title)):
        error = error + 'Name of your note must contain only letters, numbers and punctuation marks!\n'
    if not bool(re.match('^[a-zA-Z0-9,.!?]+', content)):
        error = error + 'Your note can contain only letters numbers and puctuation marks!\n'

    return error


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
