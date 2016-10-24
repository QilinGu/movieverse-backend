#!flask/bin/python
from flask import Flask, request
import api

app = Flask(__name__)

API_ROOT = "/movieverse/api/v1.0"


@app.route(API_ROOT + '/users', methods=['POST'])
def add_user():
    return api.add_user(request.json)


@app.route(API_ROOT + '/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return api.get_user_by_id(user_id)


@app.route(API_ROOT + '/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    return api.update_user_by_id(user_id, request.json)


@app.route(API_ROOT + '/users', methods=['GET'])
def get_user_by_email_search():
    email = request.args.get('email')
    return api.get_user_by_email_search(email)


@app.route(API_ROOT + '/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    return api.get_movie_by_id(movie_id)


@app.route(API_ROOT + '/movies', methods=['GET'])
def get_movies_by_name_search():
    name_string = request.args.get('name')
    return api.get_movies_by_name_search(name_string)


@app.route(API_ROOT + '/actors/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    return api.get_actor_by_id(actor_id)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0')
