#!flask/bin/python
from flask import jsonify


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
