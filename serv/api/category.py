# coding utf-8

"""
category's routers

| Function Name       | Entry Params       | Out Params     | Desc                           |
|---------------------+--------------------+----------------+--------------------------------|
| get_categories      | shop_id            | Json format CR | get category list by shop's id |
| get_category_by_id  | category_id        | same up        | get single category infor      |
| edit_category_by_id | category_id/params | same up        | edit single category infor     |
| add_category        | shop_id            | same up        | add one category to the shop   |
| del_category_by_id  | category_id        | same up        | delete current category        |

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
from flask import request
from serv.models import Category, Shop
from sqlalchemy.exc import IntegrityError


@api.route('/categories/<int:shop_id>')
def get_categories(shop_id):
    """get categories by shop's id"""
    categories = Category.query.filter_by(shop_id=shop_id).all()
    if len(categories) == 0:
        return klass_response.FailedResult('not_exist',
                                           'Category List')
    json_categories = [category.to_json() for category in categories]
    return klass_response.SuccessResult(json_categories, 200)


@api.route('/category/<int:category_id>')
def get_category_by_id(category_id):
    """get category by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return klass_response.FailedResult('not_exist',
                                           'Category')
    return klass_response.SuccessResult(category.to_json(), 200)


@api.route('/category/<int:category_id>', methods=['PUT'])
def edit_category_by_id(category_id):
    """edit category infor by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return klass_response.FailedResult('not_exist',
                                           'Category')
    category_name = request.json.get('category_name')
    order = request.json.get('order')

    if category_name is None or category_name == '':
        return klass_response.FailedResult('params_lack',
                                           'category_name')
    else:
        category.category_name = category_name

    if order is not None or order != '':
        category.order = order

    # pylint: disable=no-member
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        return klass_response.FailedResult('need_unique',
                                           'Category').to_json()
    return klass_response.SuccessResult(category.to_json(), 200).to_json()


@api.route('/category/<int:shop_id>', methods=['POST'])
def add_category(shop_id):
    """add category to shop"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('params_lack', 'shop_id')
    category_name = request.json.get('category_name')
    if category_name is None or category_name == '':
        return klass_response.FailedResult('params_lack',
                                           'category_name')
    order = request.json.get('order')
    if order is None or order == '':
        order = 0
    category = Category(category_name)
    category.order = order
    category.shop_id = shop_id
    # pylint: disable=no-member
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        return klass_response.FailedResult('need_unique',
                                           'Category').to_json()
    return klass_response.SuccessResult(category.to_json(), 200).to_json()


@api.route('/category/<int:category_id>', methods=['DELETE'])
def del_category_by_id(category_id):
    """delete category by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return klass_response.FailedResult('not_exist', 'Category')
    # pylint: disable=no-member
    db.session.delete(category)
    db.session.commit()
    return klass_response.SuccessResult(None, 200)
