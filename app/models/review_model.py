#!flask/bin/python
from flask import jsonify
import MySQLdb as MySQL

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
