#!flask/bin/python
from flask import jsonify
import MySQLdb as MySQL
import json

HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"


def add_review(review_text, sentiment):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1
    insert_query = "INSERT INTO Review(Sentiment, Review) \
        VALUES ('%d', '%s' )" % (sentiment, review_text)
    try:
        cursor.execute(insert_query)
        _id = cursor.lastrowid
        conn.commit()
        return _id
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1

def add_user_review_entry(user_id, review_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1
    insert_query = "INSERT INTO UserReview(UserID, ReviewID) \
        VALUES ('%d', '%d' )" % (user_id, review_id)
    try:
        cursor.execute(insert_query)
        _id = cursor.lastrowid
        conn.commit()
        return _id
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1


def add_movie_review_entry(movie_id, review_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1
    insert_query = "INSERT INTO MovieReview(MovieID, ReviewID) \
        VALUES ('%d', '%d' )" % (movie_id, review_id)
    try:
        cursor.execute(insert_query)
        _id = cursor.lastrowid
        conn.commit()
        return _id
    except MySQL.Error as e:
        conn.rollback()
        raise
        return -1


def get_reviews_by_movie_id(movie_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return None

    query = "SELECT ReviewID FROM Review WHERE ReviewID IN ( SELECT MovieReview.ReviewID FROM Movie1 INNER JOIN MovieReview ON MovieReview.MovieID = Movie1.MovieID WHERE Movie1.MovieID = %d )" % movie_id
    try:
        x = cursor.execute(query)
        if x == 0:
            return None

        out = []
        results = cursor.fetchall()
        for result in results:
            for _result in result:
                out.append(_result)
        return out

    except MySQL.Error as e:
        conn.rollback()
        raise
        return None

def percentage(reviewids):
    if reviewids == None:
        return None
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return None
    scores = []
    for review in reviewids:

        query = "SELECT Sentiment FROM Review WHERE ReviewID = %d" %review

        x = cursor.execute(query)
        result = cursor.fetchone()
        score = result[0]
        scores.append(score)
    total = 0
    for score in scores:
        total +=score

    ret = float(total)/len(scores)

    return ret

def get_review_by_id(review_id):
    try:
        conn = MySQL.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
        cursor = conn.cursor()
    except MySQL.Error as e:
        print "SQL Connection Error"
        conn.rollback()
        raise
        return None
    scores = []

    query = "SELECT * FROM Review WHERE ReviewID = %d" %review_id
    x = cursor.execute(query)
    review = cursor.fetchone()

    review = { "ReviewID": review[0], "TimeStamp": review[1].strftime("%Y-%m-%d %H:%M:%S"), "Sentiment": review[2], "Text": review[3]}

    query = "SELECT U.FIRST_NAME, U.LAST_NAME, U.USERID FROM USER U, UserReview UR WHERE U.UserID = UR.UserID AND UR.ReviewID = %d" %review_id
    x = cursor.execute(query)
    author = cursor.fetchone()
    author = { "UserID": author[2], "FIRST_NAME": author[0], "LAST_NAME": author[1]}



    return review, author
