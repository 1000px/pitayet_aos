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
from serv.models import Shop
from flask import request, url_for
from sqlalchemy.exc import IntegrityError


@api.route('/shops/<int:user_id>')
def get_shops_by_user_id(user_id):
    """get shop list by user's id"""
    shops = Shop.query.filter_by(owner_id=user_id).all()
    if len(shops) == 0:
        return klass_response.FailedResult('not_exist', 'Shop List')
    list_shops = [shop.to_json() for shop in shops]
    return klass_response.SuccessResult(list_shops, 200)


@api.route('/shop/<int:shop_id>')
def get_shop_by_id(shop_id):
    """get shop by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    return klass_response.SuccessResult(shop.to_json(), 200)


@api.route('/shop/<int:shop_id>', methods=['PUT'])
def edit_shop_by_id(shop_id):
    """edit current shop's infor"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    shop_name = request.json.get('shop_name')
    shop_img = request.json.get('shop_img')

    if shop_name is None and shop_img is None:
        return klass_response.FailedResult('params_lack',
                                           'shop_name, shop_img')
    if shop_name is not None:
        shop.shop_name = shop_name
    if shop_img is not None:
        shop.shop_img = shop_img
    # pylint: disable=no-member
    db.session.add(shop)
    db.session.commit()
    return klass_response.SuccessResult(shop.to_json(), 200)


@api.route('/shop', methods=['POST'])
def add_shop():
    """add new shop item"""
    shop_name = request.json.get('shop_name')
    shop_img = request.json.get('shop_img')
    user_id = request.json.get('user_id')
    shop = Shop()
    if user_id is None or user_id == '':
        return klass_response.FailedResult('params_lack', 'user_id')
    else:
        shop.owner_id = user_id

    if shop_name is None or shop_name == '':
        return klass_response.FailedResult('params_lack', 'shop_name')
    else:
        shop.shop_name = shop_name

    if shop_img is not None:
        shop.shop_img = shop_img

    # pylint: disable=no-member
    db.session.add(shop)
    try:
        db.session.commit()
    except IntegrityError:
        return klass_response.FailedResult('need_unique', 'Shop')
    return klass_response.SuccessResult(shop.to_json(), 200)


@api.route('/shop/<int:shop_id>', methods=['DELETE'])
def del_shop_by_id(shop_id):
    """delete shop by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    # pylint: disable=no-member
    db.session.delete(shop)
    db.session.commit()
    return klass_response.SuccessResult(None, 200)
