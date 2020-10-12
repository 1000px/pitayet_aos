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
from serv.api import api
from serv.utils import obj_result
from serv.models import User


@api.route('/users')
def get_users():
    """get user list"""

@api.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    """get user infor by user's id"""
    user_obj = {
        'id': user_id
    }
    res_obj = obj_result.Result(True, user_obj, 200)
    return res_obj.get_json_obj()
