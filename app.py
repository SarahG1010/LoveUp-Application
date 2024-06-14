import os
import sys
#sys.path.append("/Users/ziyuguo/Documents/AAA_job_finding/2_SDE/3_SDE_Projects/Coffee_shop_full_stack/backend/env/lib/python3.11/site-packages")

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

#from .database.models import db_drop_and_create_all, setup_db, Drink
#from .auth.auth import AuthError, requires_auth
#from database.models import db_drop_and_create_all, setup_db, Drink
#from auth.auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Drink
from auth import AuthError, requires_auth


app = Flask(__name__)
app.app_context().push()
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
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
    return greeting,200

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def show_drinks():
    all_drinks = Drink.query.all()
    ## check if drink is none 
    if not all_drinks: 
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in all_drinks]
        }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def show_drinks_details(jwt):
    all_drinks = Drink.query.all()
   
    if not all_drinks: 
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in all_drinks]
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    
    #debug use
    #print(request)
    data = request.get_json()
    #debug use
    #print(data)

    if not data:
        abort(400)

    # get data 
    new_title = data.get('title', None)
    new_recipe = data.get('recipe', None)
    #debug use
    #print(new_title)
    #print(new_recipe)
    
    if not new_title or not new_recipe:
        abort(400)

    ## for postman debug use: make sure the request data in correct format
    if not isinstance(new_recipe, list):
        abort(400)
    
    ## update drink
    new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
    try:
        new_drink.insert()
    except:
        print(Exception)
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):

    drink_update = Drink.query.get(drink_id)
    if not drink_update:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400)

    update_title = data.get('title', None)
    update_recipe = data.get('recipe', None)
    if update_title:
        drink_update.title = update_title
    if update_recipe:
        try:
            drink_update.recipe = json.dumps(update_recipe)
        except:
            print(Exception)
            abort(400)
    try:
        drink_update.update()
    except:
        print(Exception)
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink_update.long()]
    }), 200



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink_delete = Drink.query.get(drink_id)

    if not drink_delete:
        abort(404)

    try:
        drink_delete.delete()
    except:
        print(Exception)
        abort(422)

    return jsonify({
        'success': True,
        'delete': drink_delete.id
    }), 200

# Error Handling

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
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


'''
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405
'''
'''
other error handlers 
'''


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

if __name__ == '__main__':
    app.run()