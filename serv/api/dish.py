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


@api.route('/dishes/<int:shop_id>')
def get_dishes(shop_id):
    """get current shop's dish list"""
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    if page is None and per_page is None:
        # do not paginate the list
        dishes = Dish.query.all()
        count = Dish.query.count()
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
         pagination = Dish.query.paginate(
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
