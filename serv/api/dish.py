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
| hoty_dish_by_id | dish_id        | same up        | delete current dish          |

errot_types:
password_err
format_err
not_exist
account_not_active
params_err
params_lack
need_unique
"""

# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.models import Dish, Shop
from flask import request, url_for
from serv.utils import klass_response
from sqlalchemy.exc import IntegrityError


@api.route('/dishes/<int:common_id>/<string:type>')
def get_dishes(common_id, type):
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
        return klass_response.SuccessResult({
            'total': count,
            'dishes': [dish.to_json() for dish in dishes]
        }, 200)
    else:
        # get dishes by page number
        if page is None:
            page = 0
        if per_page is None:
            per_page = 10
        pagination = _query.paginate(page, per_page=per_page, error_out=False)
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
        return klass_response.SuccessResult(dish_res, 200)


@api.route('/dish/<int:dish_id>')
def get_dish_by_id(dish_id):
    """get dish by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return klass_response.FailedResult('not_exist', 'Dish')
    return klass_response.SuccessResult(dish.to_json(), 200)


@api.route('/dish/<int:dish_id>', methods=['PUT'])
def edit_dish_by_id(dish_id):
    """edit dish by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return klass_response.FailedResult('not_exist', 'Dish')
    dish_name = request.json.get('dish_name')
    dish_desc = request.json.get('dish_desc')
    dish_img = request.json.get('dish_img')

    if dish_name is None and dish_desc is None and dish_img is None:
        return klass_response.FailedResult('params_lack',
                                           'dish_name,dish_desc,dish_img')
    if dish_name is not None and dish_name != '':
        dish.dish_name = dish_name
    if dish_desc is not None and dish_desc != '':
        dish.dish_desc = dish_desc
    if dish_img is not None and dish_img != '':
        dish.dish_img = dish_img

    # pylint: disable=no-member
    db.session.add(dish)
    db.session.commit()
    return klass_response.SuccessResult(dish.to_json(), 200)


@api.route('/dish/hoty/<int:dish_id>', methods=['PUT'])
def hoty_dish_by_id(dish_id):
    """toggle dish stutas (hot or not) by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return klass_response.FailedResult('not_exist', 'Dish')
    dish.hot = not dish.hot
    # pylint: disable=no-member
    db.session.add(dish)
    db.session.commit()
    return klass_response.SuccessResult(dish.to_json(), 200)


@api.route('/dishes/<int:shop_id>', methods=['POST'])
def add_dishes(shop_id):
    """add a list of dishes to current shop"""
    # add shop exist logic's code
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    dishes_from_request = request.json.get('dishes')
    for dish in dishes_from_request:
        # pylint: disable=no-member
        o_dish = Dish()
        if dish.get('dish_name') is None or dish.get('dish_name') == '':
            return klass_response.FailedResult('params_lack', 'dish_name')
        else:
            o_dish.dish_name = dish.get('dish_name')

        if dish.get('dish_img') is None or dish.get('dish_img') == '':
            return klass_response.FailedResult('params_lack', 'dish_img')
        else:
            o_dish.dish_img = dish.get('dish_img')

        if dish.get('dish_desc') is not None or dish.get('dish_desc') != '':
            o_dish.dish_desc = dish.get('dish_desc')

        if dish.get('category_id') is not None or dish.get('category_id') != '':
            o_dish.category_id = dish.get('category_id')

        o_dish.shop_id = shop_id
        # pylint: disable=no-member
        db.session.add(o_dish)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    db.session.flush()
    return klass_response.SuccessResult(None, 200)


@api.route('/dish/<int:shop_id>', methods=['POST'])
def add_dish(shop_id):
    """add one dish to current shop"""
    # shop exist logic's code
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    dish = Dish()
    dish_name = request.json.get('dish_name')
    dish_desc = request.json.get('dish_desc')
    dish_img = request.json.get('dish_img')
    if dish_name is None or dish_name == '':
        return klass_response.FailedResult('params_lack', 'dish_name')
    else:
        dish.dish_name = dish_name
    if dish_img is None or dish_img == '':
        return klass_response.FailedResult('params_lack', 'dish_img')
    else:
        dish.dish_img = dish_img

    if dish_desc is not None:
        dish.dish_desc = dish_desc
    dish.shop_id = shop_id

    db.session.add(dish)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    db.session.flush()
    return klass_response.SuccessResult(dish.to_json(), 200)


@api.route('/dish/<int:dish_id>', methods=['DELETE'])
def del_dish_by_id(dish_id):
    """delete dish by dish's id"""
    dish = Dish.query.filter_by(id=dish_id).first()
    if dish is None:
        return klass_response.FailedResult('not_exist', 'Dish')
    # pylint: disable=no-member
    db.session.delete(dish)
    db.session.commit()
    return klass_response.SuccessResult(None, 200)
