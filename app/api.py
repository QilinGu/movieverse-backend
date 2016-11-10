#!flask/bin/python
from flask import jsonify
import requests
from bs4 import BeautifulSoup
import models
from models import user_model, movie_model, actor_model
import hashlib
import urllib2
import json
import httplib
import urllib
import base64
import sys
reload(sys)
import re

sys.setdefaultencoding('utf-8')

HOST = "127.0.0.1"
USER = "root"
PASSWORD = "cs411fa2016"
DB = "imdb"


def add_user(json_body):
    existing, message = user_model.check_existing_user(json_body['EMAIL'])
    if existing:
        return jsonify({'success': False, 'message': message})

    password = json_body['PASSWORD']
    h = hashlib.md5(password.encode())
    password = h.hexdigest()

    insert, message = user_model.add_user(json_body['FIRST_NAME'], json_body[
        'LAST_NAME'], json_body['EMAIL'], json_body['AGE'], password)

    return jsonify({'success': insert, 'message': message})


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


def get_movie_by_id(movie_id):
    success, movie, message = movie_model.get_movie_by_id(movie_id)
    actors = None
    if success:
        cover_url, thumb_url = get_movie_image_url(movie)
        movie['Poster'] = cover_url
        movie['Thumbnail'] = thumb_url
        actors = actor_model.get_actors_by_movie_id(movie_id)
    return jsonify({'success': success, 'movie': movie, 'actors': actors, 'message': message})


def get_movie_image_url(movie):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '09a829ae3d0d4e07b0cf605391d2a469',
    }
    params = urllib.urlencode({
        # Request parameters
        'q': movie['Name'] + " movie poster",
        'count': '1',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
        'size': 'Large'
    })
    cover_url = ""

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        cover_url = json.loads(data)['value'][0]["contentUrl"].encode('ISO-8859-1')
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    omdb_base = "http://www.omdbapi.com/?t="
    movie_info_omdb = urllib2.urlopen(omdb_base + movie['Name']).read()
    movie_info_omdb = json.loads(movie_info_omdb)
    return cover_url, movie_info_omdb["Poster"].encode('ISO-8859-1')


def get_movies_by_name_search(search_string):
    success, movies, message = movie_model.get_movies_by_name_search(search_string)
    return jsonify({'success': success, 'movies': movies, 'message': message})


def get_actor_by_id(actor_id):
    return jsonify({'actor_id': actor_id})
