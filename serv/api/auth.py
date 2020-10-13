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

from serv.api import api
from flask_httpauth import HTTPTokenAuth
from serv.utils import obj_result


auth = HTTPTokenAuth(scheme="Bearer")


@api.route('/register', methods=['POST'])
def register():
    """register api"""
    reg_obj = obj_result.Result(True, None, 200, 'OK').get_json_obj()
    return reg_obj


@api.route('/login', methods=['POST'])
def login():
    """login api"""
    login_obj = obj_result.Result(True, None, 200, 'OK').get_json_obj()
    return login_obj
