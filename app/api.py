#!flask/bin/python
from flask import jsonify
from bs4 import BeautifulSoup

import traceback
import requests
import hashlib
import urllib2
import json
import httplib
import urllib
import base64
import sys

import models
from models import user_model, movie_model, actor_model, director_model, review_model

import sentiment_analysis
from sentiment_analysis import sentiment

import recommendation_system
from recommendation_system import profile_builder, rec

reload(sys)
import re

sys.setdefaultencoding('utf-8')


KEYS = ["cae8ee8947314188aec462dcce894576","667b142f74de4f949c28ce442964b8a5","38a6b7556ce94984bb238b9785c556c2"]
key_index = 0
HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"

#USERS
def add_user(json_body):
    existing, message = user_model.check_existing_user(json_body['EMAIL'])
    if existing:
        return jsonify({'success': False, 'message': message})

    password = json_body['PASSWORD']
    h = hashlib.md5(password.encode())
    password = h.hexdigest()

    _id = user_model.add_user(json_body['FIRST_NAME'], json_body[
        'LAST_NAME'], json_body['EMAIL'], json_body['AGE'], password, json_body['Runtime'], json_body['Year'], json_body['Occupation'], json_body['GENDER'])

    return jsonify({'UserID': _id})


def get_user_by_id(user_id):
    success, person, message = user_model.get_user_by_id(user_id)
    return jsonify({'success': success, 'person': person, 'message': message})


def update_user_by_id(user_id, json_body):
    existing, person, message = user_model.get_user_by_id(user_id)
    if not existing:
        return jsonify({'success': False, 'message': message})
    else:
        success, message = user_model.update_user_by_id(user_id, json_body['FIRST_NAME'], json_body[
            'LAST_NAME'], json_body['AGE'])
        return jsonify({'success': success, 'message': message})


def get_user_by_email_search(email_id):
    success, person, message = user_model.get_user_by_email_search(email_id)
    return jsonify({'success': success, 'person': person, 'message': message})


#MOVIES
def get_movie_by_id(movie_id):
    success, movie, message = movie_model.get_movie_by_id(movie_id)
    directors = None
    actors = None
    if success:
        cover_url, thumb_url = get_movie_image_url(movie)
        movie['Poster'] = cover_url
        movie['Thumbnail'] = thumb_url
        actors = actor_model.get_actors_by_movie_id(movie_id)
        directors = director_model.get_directors_by_movie_id(movie_id)
        reviews = review_model.get_reviews_by_movie_id(movie_id)
        sentiment = review_model.percentage(reviews)
    return jsonify({'success': success, 'movie': movie, 'actors': actors, 'directors':directors, 'message': message, 'reviews':reviews, 'sentiment':sentiment})


def get_movie_image_url(movie):
    params = urllib.urlencode({
        # Request parameters
        'api_key': "091d974f91fed5279d0e314a34c300d3",
        'query': movie['Name']
    })
    cover_url = ""
    thumbnail_url = ""
    try:
        conn = httplib.HTTPSConnection('api.themoviedb.org')
        conn.request("GET", "/3/search/movie?%s" % params, "{body}")
        response = conn.getresponse()
        data = json.loads(response.read())
        thumbnail_url = "https://image.tmdb.org/t/p/w500/"+data['results'][0]["poster_path"].split('\/')[0].encode('ISO-8859-1')
        cover_url = "https://image.tmdb.org/t/p/w1000/"+data['results'][0]["backdrop_path"].split('\/')[0].encode('ISO-8859-1')
        conn.close()
    except Exception as e:
        traceback.print_exc()

    return cover_url, thumbnail_url


def get_movies_by_name_search(search_string):
    success, movies, message = movie_model.get_movies_by_name_search(search_string)
    return jsonify({'success': success, 'movies': movies, 'message': message})


#ACTORS
def get_actor_by_id(actor_id):
    return jsonify({'actor_id': actor_id})


#REVIEWS
def get_review_by_id(review_id):
    review ,author =  review_model.get_review_by_id(review_id)
    return jsonify({'Review':review, 'Author':author})


def add_review(json_body):
    user_id = json_body['UserID']
    movie_id = json_body['MovieID']
    text = json_body['review_text']

    #get sentiment of review
    sent = sentiment.analyse_review(text)

    #update review table
    if sent == "positive":
        binary_sent = 1
    else:
        binary_sent = 0

    _id = review_model.add_review(text, binary_sent)
    if(_id == -1):
        return jsonify({'message':'review not added', 'Error': True})

    #update user_review table
    review_model.add_user_review_entry(user_id, _id)

    #update movie_review table
    review_model.add_movie_review_entry(movie_id, _id)

    return jsonify({'message':'review added', 'ReviewID':_id, 'Error': False, 'Text': text, 'UserID':user_id, 'MovideID':movie_id})

my_ask = []

#RECOMMENDATIONS
def get_initial_reco_movies():
    sample_movies, ask = profile_builder.main_function(0, None, None, None, None, None, None)
    global my_ask
    my_ask = ask
    return jsonify({'Movies':sample_movies})


def build_user_profile(json_body):
    ratings = json_body['Ratings']
    int_ratings = []
    for rating in ratings:
        int_ratings.append(int(rating))
    print ratings, int_ratings
    user_id = json_body['UserID']
    existing, person, message = user_model.get_user_by_id(user_id)

    genres = profile_builder.main_function(1, int_ratings, person["AGE"], person["Gender"], person["Occupation"], my_ask, user_id)

    return jsonify({'Genres':genres})

def get_recommended_movies(json_body):
    user_id = json_body['UserID']
    movies, movieids = rec.tryrec(user_id)
    print movies
    print movieids

    return jsonify({'Movies': movieids})


def get_staff_picks():
    staff_list = [2872518,3029194, 3735918, 3169861, 3803644,3689621]
    return jsonify({'Movies': staff_list})
