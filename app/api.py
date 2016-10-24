#!flask/bin/python
from flask import jsonify
import models
from models import user_model, movie_model
import hashlib


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
    if success:
        actors = actor_model.get_actors_by_movie_id(movie_id)
    return jsonify({'success': success, 'movie': movie, 'actors': actors, 'message': message})


def get_movies_by_name_search(search_string):
    success, movies, message = movie_model.get_movies_by_name_search(search_string)
    return jsonify({'success': success, 'movies': movies, 'message': message})


def get_actor_by_id(actor_id):
    return jsonify({'actor_id': actor_id})
