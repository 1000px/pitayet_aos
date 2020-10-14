# coding utf-8

"""
Common class of api's result
errot_types:
password_err
format_err
not_exist
account_not_active
params_err
params_lack
need_unique
"""
from flask import jsonify

error_dict = {
    'password_err': {
        'status': 400,
        'code': 4001,
        'msg': 'wrong pasword'
    },
    'format_err': {
        'status': 400,
        'code': 4002,
        'msg': 'wrong format'
    },
    'not_exist': {
        'status': 404,
        'code': 4003,
        'msg': 'not exist'
    },
    'account_not_active': {
        'status': 400,
        'code': 4004,
        'msg': 'account not actived'
    },
    'params_err': {
        'status': 400,
        'code': 4005,
        'msg': 'params not available'
    },
    'params_lack': {
        'status': 400,
        'code': 4006,
        'msg': 'lack neccessary params'
    },
    'need_unique': {
        'status': 400,
        'code': 4007,
        'msg': 'data must unique'
    }
}



class SuccessResult():
    """Success Result class"""
    def __init__(self, obj, status_code):
        self.result = obj
        self.status_code = status_code

        self.json_result = {
            'code': self.status_code,
            'data': self.result
        }

    def to_json(self):
        """return the json result"""
        response = jsonify(self.json_result)
        response.status_code = self.status_code
        return response


class FailedResult():
    """Failed Result class"""
    def __init__(self, error_type, role):
        self.result = error_dict[error_type]
        print('1000', self.result['msg'])
        self.result['msg'] = role + ' : ' + self.result['msg']

    def to_json(self):
        response = jsonify(self.result)
        response.status_code = self.result['status']
        return response
