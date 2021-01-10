from flask import jsonify, request
from functools import wraps
from jwt import decode
from os import environ

from .aux_functions import get_user

def token_required(route):
    @wraps(route)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try: 
            data = decode(token, environ.get('SECRET_KEY'))
            print(data)
            current_user = get_user(public_id=data['public_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return route(current_user, *args, **kwargs)

    return decorated