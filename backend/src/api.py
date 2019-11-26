import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.route('/')
def hello_world():
    return jsonify({
        'success': True,
        'ping': 'pong'
    })


# ROUTES
def retrieve_drinks():
    try:
        drinks = Drink.query.order_by('id').all()
        return drinks
    except():
        abort(500)


@app.route('/drinks', methods=['GET'])
def retrieve_drinks_short():
    try:
        drinks = retrieve_drinks()
        drinks_short = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks_short,
            'total': len(drinks_short)
        })
    except():
        abort(500)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_long(payload):
    try:
        drinks = retrieve_drinks()
        drinks_long = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks_long,
            'total': len(drinks_long)
        })
    except():
        abort(401)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        body = request.get_json()

        if body == {}:
            abort(422)

        title = body.get('title', None)
        recipe = body.get('recipe', None)

        if title is None or recipe is None:
            abort(422)

        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        new_drink.insert()

        drinks = retrieve_drinks()
        drinks_short = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': drinks_short,
            'id': new_drink.id
        })

    except():
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    try:
        body = request.get_json()

        drink = Drink.query.get(drink_id)

        if drink is None:
            abort(404)

        if 'title' in body:
            drink.title = body.get('title')

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [Drink.query.get(drink.id).long()]
        })

    except():
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.get(drink_id)

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        })

    except():
        abort(404)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        'success': False,
        'error': e.status_code,
        'message': e.error
    }), e.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 403


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500
