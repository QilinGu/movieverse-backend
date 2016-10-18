#!flask/bin/python
import MySQLdb as MySQL
import hashlib


try:
    conn = MySQL.connect(host="127.0.0.1", user="root", passwd="cs411fa2016", db="imdb")
    cursor = conn.cursor()
except MySQL.Error as e:
    print "SQL Connection Error"
    conn.rollback()
    raise

def add_user(first_name, last_name, email, age, password):
    h = hashlib.md5(password.encode())
    password = h.hexdigest()

    check_query = "SELECT * FROM USER WHERE EMAIL = '%s'" % email
    try:
        x = cursor.execute(check_query)
        if x > 0:
            print "Email already in use"
        else:
            insert_query = "INSERT INTO USER(FIRST_NAME, LAST_NAME, EMAIL, AGE, PASSWORD) \
                VALUES ('%s', '%s', '%s', '%d', '%s' )" % (first_name, last_name, email, age, password)
            try:
                cursor.execute(insert_query)
                conn.commit()
            except MySQL.Error as e:
                print "error with:"
                print insert_query
                conn.rollback()
                raise
    except MySQL.Error as e:
        print "SQL Error"
        conn.rollback()
        raise
