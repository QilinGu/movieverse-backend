#!flask/bin/python
import json
from flask import jsonify
import MySQLdb as MySQL

HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"


def get_directors_by_movie_id(movie_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return None

    query = "SELECT Name, DirectorID FROM Director WHERE DirectorID IN ( SELECT MovieDirector.DirectorID FROM Movie INNER JOIN MovieDirector ON MovieDirector.MovieID = Movie.MovieID WHERE Movie.MovieID = %d )" % movie_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return None

        results = cursor.fetchall()

        directors = []
        for result in results:
            director_id = result[1]
            director_name = result[0]

            director = {"DirectorID": director_id, "Name": director_name}
            directors.append(director)

        directors = json.dumps(directors, ensure_ascii=False)
        return directors

    except MySQL.Error as e:
        conn.rollback()
        raise
        return None
