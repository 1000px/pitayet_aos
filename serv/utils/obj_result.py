# coding utf-8

"""
Common class of api's result
"""
from flask import jsonify

class Result():
    """Result"""
    is_success = False
    res_obj = None
    """The init function"""
    def __init__(self, is_success, obj, status_code):
        self.is_success = is_success
        self.res_obj = obj
        self.status_code = status_code
        res_str = 'failed'
        if self.is_success:
            res_str = 'success'
        self.json_obj = {
            'res': res_str,
            'data': self.res_obj
        }

    def get_json_obj(self):
        """return the json result"""
        response = jsonify(self.json_obj)
        response.status_code = self.status_code
        return response
