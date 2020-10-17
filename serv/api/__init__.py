# coding utf-8

"""
You can edit the server api's logic code
"""
from flask import Blueprint

api = Blueprint('api', __name__)

"""do not check this import code"""
# pylint: disable=all
from . import user
from . import shop
from . import dish
from . import category
from . import order

from . import auth
