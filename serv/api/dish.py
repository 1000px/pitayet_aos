# coding utf-8

"""
dish's routers
| Function Name   | Entry Params   | Out Params     | Desc                         |
|-----------------+----------------+----------------+------------------------------|
| get_dishes      | shop_id        | Json format CR | get dish list by shop's id   |
| get_dishes      | category_id    | Json format CR | get dish list by shop's id   |
| get_dish_by_id  | dish_id        | same up        | get single dish infor        |
| edit_dish_by_id | dish_id/params | same up        | edit single dish infor       |
| add_dishes      | list/shop_id   | same up        | add a few dishes to the shop |
| del_dish_by_id  | dish_id        | same up        | delete current dish          |
"""

# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.models import Dish, Shop
from flask import request, url_for
from serv.utils import obj_result


@api.route('/dishes/<int:common_id>/<string:type>')
def get_dishes(shop_id, type):
    """get current shop's dish list"""
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    # type: category or all
    _query = None
    if type == 'all':
        _query = Dish.query.filter_by(shop_id=common_id)
    if type == 'category':
        _query = Dish.query.filter_by(category_id=common_id)

    if page is None and per_page is None:
        # do not paginate the list
        dishes = _query.all()
        count = _query.count()
        return obj_result.Result(True, {
            'total': count,
            'dishes': dishes
        }, 200, 'OK').get_json_obj()
    else:
        # get dishes by page number
        if page is None:
            page = 0
        if per_page is None:
            per_page = 10
         pagination = _query.paginate(
            page,
            per_page=per_page,
            error_out=False
        )
        dishes = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_dishes', page=page-1, per_page=per_page)
        nextu = None
        if pagination.has_next:
            nextu = url_for('api.get_dishes', page=page+1, per_page=per_page)
        dish_res = {
            'prev_url': prev,
            'next_url': nextu,
            'total': pagination.total,
            'dishes': [dish.to_json() for dish in dishes]
        }
        return obj_result.Result(True, dish_res, 200, 'OK').get_json_obj()


@api.route('/dish/<int:dish_id>')
def get_dish_by_id(dish_id):
    """get dish by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return obj_result.Result(False, None, 404,
                                 'Dish Not Found.').get_json_obj()
    return obj_result.Result(True, dish.to_json(), 200, 'OK').get_json_obj()


@api.route('/dish/<int:dish_id>', methods=['PUT'])
def edit_dish_by_id(dish_id):
    """edit dish by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return obj_result.Result(False, None, 404,
                                 'Dish Not Found.').get_json_obj()
