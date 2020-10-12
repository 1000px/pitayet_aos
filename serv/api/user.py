# coding utf-8

"""
The user's routers
| Function Name   | Entry Params            | Out Params     | Desc                                   |
|-----------------+-------------------------+----------------+----------------------------------------|
| get_users       |                         | Json format CR | get user list                          |
| get_user_by_id  | user_id                 | same up        | get user infor by user's id            |
| edit_user_by_id | username/user_id/...    | same up        | edit user infor by user's id           |
| del_user_by_id  | user_id                 | same up        | delete current user                    |
"""
# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.utils import obj_result
from serv.models import User
from flask import request, url_for


@api.route('/users')
def get_users():
    """get user list by pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = User.query.paginate(
        page,
        per_page=per_page,
        error_out=False
    )
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1, per_page=per_page)
    nextu = None
    if pagination.has_next:
        nextu = url_for('api.get_users', page=page+1, per_page=per_page)

    data_obj = {
        'users': [user.to_json() for user in users],
        'prev_url': prev,
        'next_url': nextu,
        'total': pagination.total
    }
    return obj_result.Result(True, data_obj, 200, 'OK').get_json_obj()


@api.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    """get user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return obj_result.Result(False, None, 404,
                                 'User Not Found.').get_json_obj()

    user_obj = user.to_json()
    res_obj = obj_result.Result(True, user_obj, 200, 'OK')
    return res_obj.get_json_obj()


@api.route('/user/<int:user_id>', methods=['PUT'])
def edit_user_by_id(user_id):
    """edit user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return obj_result.Result(False, None, 404,
                                 'User Not Found.').get_json_obj()

    user_name = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role')

    if user_name is None and password is None and role is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessay Params').get_json_obj()
    if user_name is not None:
        user.user_name = user_name
    if password is not None:
        user.password = password
    if role is not None:
        user.role = role

    # pylint: disable=no-member
    db.session.add(user)
    db.session.commit()
    return obj_result.Result(True, user, 200, 'OK').get_json_obj()


@api.route('/user/<int:user_id>', methods=['DELETE'])
def del_user_by_id(user_id):
    """delete user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return obj_result.Result(False, None, 404,
                                 'User Not Found.').get_json_obj()
    # pylint: disable=no-member
    db.session.delete(user)
    db.session.commit()
    return obj_result.Result(True, None, 200,
                             'Delete User Success.').get_json_obj()
