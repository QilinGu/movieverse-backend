#!flask/bin/python
from flask import jsonify
import MySQLdb as MySQL


try:
    conn = MySQL.connect(host="127.0.0.1", user="root", passwd="cs411fa2016", db="imdb")
    cursor = conn.cursor()
except MySQL.Error as e:
    print "SQL Connection Error"
    conn.rollback()
    raise


def check_existing_user(email):
    check_query = "SELECT * FROM USER WHERE EMAIL = '%s'" % email
    try:
        x = cursor.execute(check_query)
        if x != 0:
            return True, "User Exists"
        return False, None
    except MySQL.Error as e:
        conn.rollback()
        raise
        return True, "SQL connection error"


def add_user(first_name, last_name, email, age, password):
    insert_query = "INSERT INTO USER(FIRST_NAME, LAST_NAME, EMAIL, AGE, PASSWORD) \
        VALUES ('%s', '%s', '%s', '%d', '%s' )" % (first_name, last_name, email, age, password)
    try:
        cursor.execute(insert_query)
        conn.commit()
        return True, "User added successfully"
    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, "MySQL error"


def update_user_by_id(user_id, first_name, last_name, age):
    update_query = "UPDATE USER SET FIRST_NAME='%s', LAST_NAME='%s',  AGE='%d' WHERE USERID='%d'" % (
        first_name, last_name, age, user_id)
    try:
        cursor.execute(update_query)
        conn.commit()
        return True, "User updated successfully"
    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, "MySQL error"


def get_user_by_id(user_id):
    query = "SELECT * FROM USER WHERE USERID = " + str(user_id)
    print user_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return False, None, "No such user exists"

        result = cursor.fetchone()

        userid = result[0]
        first_name = result[1]
        last_name = result[2]
        email = result[3]
        age = result[4]

        person = {"USERID": userid, "FIRST_NAME": first_name,
                  "LAST_NAME": last_name, "EMAIL": email, "AGE": age}

        return True, person, "Person found"

    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"


def get_user_by_email_search(email_id):
    query = "SELECT * FROM USER WHERE EMAIL = '%s'" % email_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return False, None, "No such user exists"

        result = cursor.fetchone()

        userid = result[0]
        first_name = result[1]
        last_name = result[2]
        email = result[3]
        age = result[4]

        person = {"USERID": userid, "FIRST_NAME": first_name,
                  "LAST_NAME": last_name, "EMAIL": email, "AGE": age}

        return True, person, "Person found"

    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"
