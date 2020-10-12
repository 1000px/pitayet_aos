# coding utf-8

"""
the error result of all apis
"""
from flask import jsonify


def bad_request(message):
    """response for bad_request"""
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    """response for unauthorized"""
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    """response for forbidden"""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response
