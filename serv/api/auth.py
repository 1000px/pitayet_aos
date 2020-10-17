# coding utf-8

"""
login and register
you can get a timeout token code after login
| Function Name   | Entry Params            | Out Params     | Desc                                   |
|-----------------+-------------------------+----------------+----------------------------------------|
| register        | username/email/password | Json format CR | register new account                   |
| login           | username/password       | same up        |                                        |
| active          |                         | active link    | return one active link to current user |

errot_types:
password_err
format_err
not_exist
account_not_active
params_err
params_lack
"""
from serv import db
from serv.api import api
from serv.models import User
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.exc import IntegrityError
from serv.utils import klass_response
from flask import request
import re


auth = HTTPTokenAuth(scheme="Bearer")


@api.route('/register', methods=['POST'])
def register():
    """register api"""
    user_name = request.json.get('user_name')
    pat_user_name = r'^[0-9a-zA-Z_]{4,18}$'
    if re.match(pat_user_name, user_name) is None:
        return klass_response.FailedResult('format_err', 'user name')

    password = request.json.get('password')
    pat_password = r'^[0-9a-zA-Z_]{6,20}$'
    if re.match(pat_password, password) is None:
        return klass_response.FailedResult('format_err', 'password')

    email = request.json.get('email')
    pat_email = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(pat_email, email) is None:
        return klass_response.FailedResult('format_err', 'email')
    my = User()
    my.user_name = user_name
    my.password = password
    my.email = email

    # pylint: disable=no-member
    db.session.add(my)
    try:
        db.session.commit()
    except IntegrityError:
        return klass_response.FailedResult('params_err',
                                           'mysql commit')

    return klass_response.SuccessResult(my.to_json(), 200)


@api.route('/login', methods=['POST'])
def login():
    """login api"""
    # whether or not this count is already actived
    user_name = request.json.get('user_name')
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        return klass_response.FailedResult('not_exist', 'User')
    if not user.disabled:
        return klass_response.FailedResult('account_not_active',
                                           user.user_name)

    password = request.json.get('password')
    if not user.verify_password(password):
        return klass_response.FailedResult('password_err',
                                           user.user_name)

    return klass_response.SuccessResult(user.to_json(), 200)
