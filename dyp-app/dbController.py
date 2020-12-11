import sqlite3


def insertUser(user_login, user_password, user_email):
    try:
        print("Trying to insert User")
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO users
                          (user_login, user_password, user_email) 
                          VALUES (?, ?, ?);"""

        data_tuple = (user_login, user_password, user_email)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def insertNote(user_id, note_private, note_title, note_text):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO notes
                          (note_id, user_id, note_private, note_title, note_text) 
                          VALUES (NULL, ?, ?, ?, ?);"""

        data_tuple = (user_id, note_private, note_title, note_text)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getUserByLogin(user_login):
    try:
        print("Trying to get user")
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from users where user_login = ?"""
        cursor.execute(sqlite_select_query, (user_login,))
        record = cursor.fetchone()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
        return None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getUserById(user_id):
    try:
        print("Trying to get user")
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from users where user_id = ?"""
        cursor.execute(sqlite_select_query, (user_id,))
        record = cursor.fetchone()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
        return None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getAllPublicNotes():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select note_id, note_title from notes where note_private = ?"""
        cursor.execute(sql_select_query, (0,))
        records = cursor.fetchall()
        cursor.close()

        return records

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getUserNotes(user_id):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select note_id, note_title, note_private from notes where user_id = ?"""
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        cursor.close()

        return records

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def getNote(note_id):
    try:
        print("Trying to get user")
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from notes where note_id = ?"""
        cursor.execute(sqlite_select_query, (note_id,))
        record = cursor.fetchone()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
        return None
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def updatePassword(user_id, user_password):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """Update users set user_password = ? where user_id = ?"""
        data = (user_password, user_id)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The sqlite connection is closed")




