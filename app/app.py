#!flask/bin/python
from flask import Flask, request
import api

app = Flask(__name__)

API_ROOT = "/movieverse/api/v1.0"


@app.route(API_ROOT + '/users', methods=['POST'])
def add_user():
    return api.add_user(request.json);

@app.route(API_ROOT + '/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    return api.get_movie_by_id(movie_id)


@app.route(API_ROOT + '/movies', methods=['GET'])
def get_movie_by_name_search():
    name_string = request.args.get('name')
    return api.get_movie_by_name_search(name_string)


@app.route(API_ROOT + '/actors/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    return api.get_actor_by_id(actor_id)


@app.route(API_ROOT + '/actors', methods=['GET'])
def get_actor_by_name_search():
    name_string = request.args.get('name')
    return api.get_actor_by_name_search(name_string)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
