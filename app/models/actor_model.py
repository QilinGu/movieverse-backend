#!flask/bin/python
import json
from flask import jsonify
import MySQLdb as MySQL


try:
    conn = MySQL.connect(host="127.0.0.1", user="root", passwd="cs411fa2016", db="imdb")
    cursor = conn.cursor()
except MySQL.Error as e:
    print "SQL Connection Error"
    conn.rollback()
    raise


def get_actors_by_movie_id(movie_id):
    query = "SELECT Name, ActorID FROM Actor WHERE ActorID IN ( SELECT MovieActor.ActorID FROM Movie INNER JOIN MovieActor ON MovieActor.MovieID = Movie.MovieID WHERE Movie.MovieID = %d )" % movie_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return None

        results = cursor.fetchall()

        actors = []
        for result in results:
            actor_id = result[0]
            actor_name = result[1]

            actor = {"ActorID": actor_id, "Name": actor_name}
            actors.append(actor)

        actors = json.dumps(actors, ensure_ascii=False)
        return actors

    except MySQL.Error as e:
        conn.rollback()
        raise
        return False, None, "SQL connection error"
