#!flask/bin/python
import json
from flask import jsonify
import MySQLdb as MySQL

HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"


def get_movie_by_id(movie_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return False, None, "SQL connection error"
    query = "SELECT * FROM Movie WHERE MovieID = " + str(movie_id)
    try:
        x = cursor.execute(query)
        if x == 0:
            return False, None, "No such movie exists"

        result = cursor.fetchone()

        movie_id = result[0]
        synopsis = result[1]
        movie_name = result[2]
        runtime = result[3]
        imdb_rating = result[4]

        movie = {"MovieID": movie_id, "Synopsis": synopsis, "Name": movie_name, "Runtime": runtime, "IMDB_rating": imdb_rating }

        return True, movie, "Movie found"

    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"


def get_movies_by_name_search(movie_name):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return False, None, "SQL connection error"
    query = "SELECT * FROM Movie WHERE Name LIKE '%%%s%%'" % movie_name
    try:
        x = cursor.execute(query)
        if x == 0:
            return False, None, "No such movie exists"

        results = cursor.fetchall()

        movie_list = []

        for result in results:
            movie_id = result[0]
            synopsis = result[1]
            movie_name = result[2]
            runtime = result[3]
            imdb_rating = result[4]

            movie = {"MovieID": movie_id, "Synopsis": synopsis, "Name": movie_name, "Runtime": runtime, "IMDB_rating": imdb_rating }
            movie_list.append(movie)

        movie_list = json.dumps(movie_list, ensure_ascii = False)
        return True, movie_list, "Movie/s found"

    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"
