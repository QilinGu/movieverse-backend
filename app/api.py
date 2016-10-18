#!flask/bin/python
from flask import jsonify
import models


def add_user(json_body):
    models.add_user(json_body['FIRST_NAME'], json_body[
                    'LAST_NAME'], json_body['EMAIL'], json_body['AGE'], json_body['PASSWORD'])
    return jsonify({'movie_id': "test"})


def get_movie_by_id(movie_id):
    return jsonify({'movie_id': movie_id})


def get_movie_by_name_search(search_string):
    if search_string:
        return jsonify({'name_string': search_string})
    else:
        return jsonify({'name_string': "Undefined"})


def get_actor_by_id(actor_id):
    return jsonify({'actor_id': actor_id})


def get_actor_by_name_search(search_string):
    if search_string:
        return jsonify({'name_string': search_string})
    else:
        return jsonify({'name_string': "Undefined"})
