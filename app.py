import os
import sys

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

#from .database.models import db_drop_and_create_all, setup_db, Drink
#from .auth.auth import AuthError, requires_auth
#from database.models import db_drop_and_create_all, setup_db, Drink
#from auth.auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Movie, Pred_Rating
from auth import AuthError, requires_auth

'''
app = Flask(__name__)
app.app_context().push()
setup_db(app)
CORS(app)
'''

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    #### important revision!!!
    app.app_context().push()

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    
    '''
    Running this funciton will add one row to each table
    '''
    db_drop_and_create_all()

    # ROUTES
    '''
    Root route
        GET /
            it should be a public endpoint
    '''
    @app.route('/')
    def get_greeting():
        greeting = "Hello" 
        return jsonify({
            'success': True,
            'message': greeting
            }), 200

    '''
        GET /movies
    '''
    @app.route('/movies', methods=['GET'])
    def show_movies():
        all_movies = Movie.query.all()
        ## check if movie is none 
        if not all_movies: 
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.short_format() for movie in all_movies]
            }), 200


    '''
        GET /movies-detail
    '''
    @app.route('/movies-detail', methods=['GET'])
    @requires_auth('get:movies-detail')
    def show_movies_details(jwt):
    #def show_movies_details():
        all_movies = Movie.query.all()
    
        if not all_movies: 
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.long_format() for movie in all_movies]
        }), 200

    '''
        POST /movies
        post requst format:
        {
      "detail": [{"director": "AA", "writer": "a1, b1", "Cast": "a2, b2"}],
      "duration": 120,
      "pred_rating_id": 1,
      "title": "test1",
      "year": 1990
    }
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
    #def add_movie():
        
        #debug use
        #print(request)
        data = request.get_json()
        #debug use
        print(data)

        if not data:
            abort(400)

        # get data 
        new_title = data.get('title', None)
        new_detail = data.get('detail', None)
        new_year = data.get('year', None)
        new_duration = data.get('duration', None)
        new_pred_rating_id = data.get('pred_rating_id', None)
        #debug use
        print(new_title)
        print(new_detail)
        
        if not new_title or not new_year or not new_detail or not new_duration or not new_pred_rating_id:
            abort(400)

        ## for postman debug use: make sure the request data in correct format
        if not isinstance(new_detail, list):
            abort(400)
        
        ## update drink
        new_movie = Movie(
            title=new_title, 
            detail=json.dumps(new_detail),
            year = new_year,
            duration = new_duration,
            pred_rating_id = new_pred_rating_id,
            )
        try:
            new_movie.insert()
        except:
            print(Exception)
            abort(422)

        return jsonify({
            'success': True,
            'movies': [new_movie.long_format()]
        }), 200


    '''
        PATCH /movies/<id>
    '''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
    #def update_movie(movie_id):

        movie_update = Movie.query.get(movie_id)
        if not movie_update:
            abort(404)

        data = request.get_json()
        if not data:
            abort(400)

        update_title = data.get('title', None)
        update_detail = data.get('detail', None)
        update_year = data.get('year', None)
        update_duration = data.get('duration', None)
        update_pred_rating_id = data.get('pred_rating_id', None)
        
        if update_title:
            movie_update.title = update_title
        if update_detail:
            try:
                movie_update.detail = json.dumps(update_detail)
            except:
                print(Exception)
                abort(400)
        if update_year:
            movie_update.year = update_year
        if update_duration:
            movie_update.duration = update_duration
        if update_pred_rating_id:
            movie_update.pred_rating_id = update_pred_rating_id
        try:
            movie_update.update()
        except:
            print(Exception)
            abort(422)

        return jsonify({
            'success': True,
            'movies': [movie_update.long_format()]
        }), 200


    '''
        DELETE /movies/<id>
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_drink(jwt, movie_id):
    #def delete_drink(movie_id):
        movie_delete = Movie.query.get(movie_id)

        if not movie_delete:
            abort(404)

        try:
            movie_delete.delete()
        except:
            print(Exception)
            abort(422)

        return jsonify({
            'success': True,
            'delete': movie_delete.id
        }), 200




    # Error Handling

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404


    '''
    implement error handler for AuthError
    '''
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'
        }), 403


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400



    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Content"
        }), 422


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)