#!flask/bin/python
import json
from flask import jsonify
import MySQLdb as MySQL

HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"


def get_actors_by_movie_id(movie_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return None

    query = "SELECT Name, ActorID FROM Actor1 WHERE ActorID IN ( SELECT MovieActor1.ActorID FROM Movie1 INNER JOIN MovieActor1 ON MovieActor1.MovieID = Movie1.MovieID WHERE Movie1.MovieID = %d )" % movie_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return None

        results = cursor.fetchall()

        actors = []
        for result in results:
            actor_id = result[1]
            actor_name = result[0]

            actor = {"ActorID": actor_id, "Name": actor_name}
            actors.append(actor)

        actors = json.dumps(actors, ensure_ascii=False)
        return actors

    except MySQL.Error as e:
        conn.rollback()
        raise
        return None
