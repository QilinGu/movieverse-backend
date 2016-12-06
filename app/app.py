#!flask/bin/python
from flask import Flask, request
from flask_cors import CORS, cross_origin
import api

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

API_ROOT = "/movieverse/api/v1.0"



#USERS
@app.route(API_ROOT + '/users', methods=['POST'])
@cross_origin(origin='*')
def add_user():
    return api.add_user(request.json)


@app.route(API_ROOT + '/users/<int:user_id>', methods=['GET'])
@cross_origin(origin='*')
def get_user_by_id(user_id):
    return api.get_user_by_id(user_id)

@app.route(API_ROOT + '/users/<int:user_id>', methods=['PUT'])
@cross_origin(origin='*')
def update_user_by_id(user_id):
    return api.update_user_by_id(user_id, request.json)


@app.route(API_ROOT + '/users', methods=['GET'])
@cross_origin(origin='*')
def get_user_by_email_search():
    email = request.args.get('email')
    return api.get_user_by_email_search(email)


#MOVIES
@app.route(API_ROOT + '/movies/<int:movie_id>', methods=['GET'])
@cross_origin(origin='*')
def get_movie_by_id(movie_id):
    return api.get_movie_by_id(movie_id)


@app.route(API_ROOT + '/movies', methods=['GET'])
@cross_origin(origin='*')
def get_movies_by_name_search():
    name_string = request.args.get('name')
    return api.get_movies_by_name_search(name_string)


#ACTORS
@app.route(API_ROOT + '/actors/<int:actor_id>', methods=['GET'])
@cross_origin(origin='*')
def get_actor_by_id(actor_id):
    return api.get_actor_by_id(actor_id)


#REVIEWS
@app.route(API_ROOT + '/reviews/<int:review_id>', methods=['GET'])
@cross_origin(origin='*')
def get_review_by_id(review_id):
    return api.get_review_by_id(review_id)


@app.route(API_ROOT + '/reviews', methods=['POST'])
@cross_origin(origin='*')
def add_review():
    return api.add_review(request.json)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0')
