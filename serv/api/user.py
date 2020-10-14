# coding utf-8

"""
The user's routers
| Function Name   | Entry Params            | Out Params     | Desc                                   |
|-----------------+-------------------------+----------------+----------------------------------------|
| get_users       |                         | Json format CR | get user list                          |
| get_user_by_id  | user_id                 | same up        | get user infor by user's id            |
| edit_user_by_id | username/user_id/...    | same up        | edit user infor by user's id           |
| del_user_by_id  | user_id                 | same up        | delete current user                    |

errot_types:
password_err
format_err
not_exist
account_not_active
params_err
params_lack
"""
# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.utils import klass_response
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
    return klass_response.SuccessResult(data_obj, 200).to_json()


@api.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    """get user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return klass_response.FailedResult('not_exist', 'User').to_json()

    return klass_response.SuccessResult(user.to_json(), 200).to_json()


@api.route('/user/<int:user_id>', methods=['PUT'])
def edit_user_by_id(user_id):
    """edit user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return klass_response.FailedResult('not_exist', 'User').to_json()

    user_name = request.json.get('user_name')
    role = request.json.get('role')

    if user_name is None or user_name == '':
        return klass_response.FailedResult('params_lack',
                                           'user_name').to_json()
    user.user_name = user_name
    if role is not None and role != '':
        user.role = role

    # pylint: disable=no-member
    db.session.add(user)
    db.session.commit()
    return klass_response.SuccessResult(user.to_json(), 200).to_json()


@api.route('/user/<int:user_id>', methods=['DELETE'])
def del_user_by_id(user_id):
    """delete user infor by user's id"""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return klass_response.FailedResult('not_exist', 'User').to_json()
    # pylint: disable=no-member
    db.session.delete(user)
    db.session.commit()
    return klass_response.SuccessResult(None, 200).to_json()
