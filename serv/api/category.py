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
"""
# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.utils import obj_result
from flask import request
from serv.models import Category, Shop


@api.route('/categories/<int:shop_id>')
def get_categories(shop_id):
    """get categories by shop's id"""
    categories = Category.query.filter_by(shop_id=shop_id).all()
    if len(categories) == 0:
        return obj_result.Result(False, None, 404,
                                 'Category List is Null').get_json_obj()
    json_categories = [category.to_json() for category in categories]
    return obj_result.Result(True, json_categories, 200,
                             'OK').get_json_obj()


@api.route('/category/<int:category_id>')
def get_category_by_id(category_id):
    """get category by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return obj_result.Result(False, None, 404,
                                 'Category Not Found.').get_json_obj()
    return obj_result.Result(True, category, 200, 'OK').get_json_obj()


@api.route('/category/<int:category_id>', methods=['PUT'])
def edit_category_by_id(category_id):
    """edit category infor by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return obj_result.Result(False, None, 404,
                                 'Category Not Found.').get_json_obj()
    category_name = request.json.get('category_name')
    order = request.json.get('order')

    if category_name is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessary Params: category_name').get_json_obj()
    else:
        category.category_name = category_name

    if order is not None:
        category.order = order

    # pylint: disable=no-member
    db.session.add(category)
    db.session.commit()
    return obj_result.Result(True, category.to_json(), 200,
                             'OK').get_json_obj()


@api.route('/category/<int:shop_id>', methods=['POST'])
def add_category(shop_id):
    """add category to shop"""
    shop = Shop.query.filter_by(shop_id=shop_id).first()
    if shop is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessary Params: shop_id').get_json_obj()
    category_name = request.json.get('category_name')
    if category_name is None:
        return obj_result.Result(False, None, 400,
                                 'Need Neccessary Params: category_name').get_json_obj()
    order = request.json.get('order')
    if order is None:
        order = 0
    category = Category(category_name)
    category.order = order
    category.shop_id = shop_id
    # pylint: disable=no-member
    db.session.add(category)
    db.session.commit()
    return obj_result.Result(True, category.to_json(), 200,
                             'OK').get_json_obj()


@api.route('/category/<int:category_id>', methods=['DELETE'])
def del_category_by_id(category_id):
    """delete category by category's id"""
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return obj_result.Result(False, None, 400,
                                 'Current Category is not exist.').get_json_obj()
    # pylint: disable=no-member
    db.session.delete(category)
    db.session.commit()
    return obj_result.Result(True, None, 200,
                             'Delete Category Success.').get_json_obj()
