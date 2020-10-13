# coding utf-8

"""
shop's routers
| Function Name   | Entry Params               | Out Params     | Desc                         |
|-----------------+----------------------------+----------------+------------------------------|
| get_shops_by_user_id| user_id                | Json format CR | get current user's shop list |
| get_shop_by_id  | shop_id                    | Json format CR | get shop infor by shop_id    |
| edit_shop_by_id | shop_id/params             | Json format CR | edit your shop infor         |
| add_shop        | shop_name/shop_img/owner_id | Json format CR | add a new shop              |
| del_shop_by_id  | shop_id                    | same up        | delete current shop          |
"""

# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.utils import obj_result
from serv.models import Shop
from flask import request, url_for
from sqlalchemy.exc import IntegrityError


@api.route('/shops/<int:user_id>')
def get_shops_by_user_id(user_id):
    """get shop list by user's id"""
    shops = Shop.query.filter_by(owner_id=user_id).all()
    if len(shops) == 0:
        return obj_result.Result(False, None, 404,
                                 'Shop List is Null.').get_json_obj()
    list_shops = [shop.to_json() for shop in shops]
    return obj_result.Result(True, list_shops, 200,
                             'Ok').get_json_obj()


@api.route('/shop/<int:shop_id>')
def get_shop_by_id(shop_id):
    """get shop by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return obj_result.Result(False, None, 404,
                                 'Shop Not Found.').get_json_obj()
    return obj_result.Result(True, shop.to_json(), 200,
                             'OK').get_json_obj()


@api.route('/shop/<int:shop_id>', methods=['PUT'])
def edit_shop_by_id(shop_id):
    """edit current shop's infor"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return obj_result.Result(False, None, 404,
                                 'Shop Not Found.').get_json_obj()
    shop_name = request.json.get('shop_name')
    shop_img = request.json.get('shop_img')

    if shop_name is None and shop_img is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessay Params').get_json_obj()
    if shop_name is not None:
        shop.shop_name = shop_name
    if shop_img is not None:
        shop.shop_img = shop_img
    # pylint: disable=no-member
    db.session.add(shop)
    db.session.commit()
    return obj_result.Result(True, shop.to_json(), 200,
                             'OK').get_json_obj()


@api.route('/shop', methods=['POST'])
def add_shop():
    """add new shop item"""
    shop_name = request.json.get('shop_name')
    shop_img = request.json.get('shop_img')
    user_id = request.json.get('user_id')
    print('1000---->>', user_id)
    shop = Shop()
    if user_id is None or user_id == '':
        return obj_result.Result(False, None, 400,
                                 'Need Neccessary Params: user_id').get_json_obj()
    else:
        shop.owner_id = user_id

    if shop_name is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessary Prams: shop_name').get_json_obj()
    else:
        shop.shop_name = shop_name

    if shop_img is not None:
        shop.shop_img = shop_img

    # pylint: disable=no-member
    db.session.add(shop)
    try:
        db.session.commit()
    except IntegrityError:
        return obj_result.Result(False, 'IntegrityError', 400,
                                 'Params Not Available.').get_json_obj()
    return obj_result.Result(True, shop.to_json(), 200,
                             'OK').get_json_obj()


@api.route('/shop/<int:shop_id>', methods=['DELETE'])
def del_shop_by_id(shop_id):
    """delete shop by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return obj_result.Result(False, None, 404,
                                 'Shop Not Found.').get_json_obj()
    # pylint: disable=no-member
    db.session.delete(shop)
    db.session.commit()
    return obj_result.Result(True, None, 200,
                             'Delete Shop Success.').get_json_obj()
