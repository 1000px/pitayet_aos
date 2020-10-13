# coding utf-8

"""
login and register
you can get a timeout token code after login
| Function Name   | Entry Params            | Out Params     | Desc                                   |
|-----------------+-------------------------+----------------+----------------------------------------|
| register        | username/email/password | Json format CR | register new account                   |
| login           | username/password       | same up        |                                        |
| active          |                         | active link    | return one active link to current user |
"""
from serv import db
from serv.api import api
from serv.models import User
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.exc import IntegrityError
from serv.utils import obj_result
from flask import request
import re


auth = HTTPTokenAuth(scheme="Bearer")


@api.route('/register', methods=['POST'])
def register():
    """register api"""
    user_name = request.json.get('user_name')
    pat_user_name = r'^[0-9a-zA-Z_]{4,18}$'
    if re.match(pat_user_name, user_name) is None:
        return obj_result.Result(False, None, 400,
                                 'Wrong UserName Format.').get_json_obj()

    password = request.json.get('password')
    pat_password = r'^[0-9a-zA-Z]{6, 20}$'
    if re.match(pat_password, password) is None:
        return obj_result.Result(False, None, 400,
                                 'Wrong Password Format.').get_json_obj()

    email = request.json.get('email')
    pat_email = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(pat_email, email) is None:
        return obj_result.Result(False, None, 400,
                                 'Wrong Email Format.').get_json_obj()
    my = User()
    my.user_name = user_name
    my.password = password
    my.email = email

    # pylint: disable=no-member
    db.session.add(my)
    try:
        db.session.commit()
    except IntegrityError:
        return obj_result.Result(False, 'IntegrityError', 400,
                                 'Params Not Available').get_json_obj()
    return obj_result.Result(True, my.to_json(), 200,
                             'You need to active this account before using it.').get_json_obj()


@api.route('/login', methods=['POST'])
def login():
    """login api"""
    # whether or not this count is already actived
    user_name = request.json.get('user_name')
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        return obj_result.Result(False, None, 400,
                                 'User Not Exist.').get_json_obj()
    if not user.disabled:
        return obj_result.Result(False, None, 204,
                                 'You must active this account first.').get_json_obj()

    password = request.json.get('password')
    if not user.verify_password(password):
        return obj_result.Result(False, None, 400,
                                 'Password Not Correct.').get_json_obj()

    return obj_result.Result(True, user.to_json(), 200, 'OK').get_json_obj()
