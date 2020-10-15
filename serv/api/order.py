# coding utf-8
"""
order's api file

| Function Name       | Entry Params | Out Params     | Desc                           |
|---------------------+--------------+----------------+--------------------------------|
| get_orders          | shop_id      | Json format CR | get order list by shop's id    |
| get_order_by_id     | order_id     | same up        | get single order infor         |
| edit_order_by_id    | order_id     | same up        | edit order detail              |
| update_order_dishes | order_id     | same up        | update dish list of this order |
| get_dishes_of_order | order_id     | same up        | get dishes of this order       |
"""
# pylint: disable=import-error
from serv import db
from serv.api import api
from serv.utils import klass_response, bowl
from flask import request, url_for, jsonify
from serv.models.order import Order
from serv.models.shop import Shop


@api.route('/orders/<int:shop_id>')
def get_orders(shop_id):
    """get order list by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop').to_json()
    page = request.get('page', 1, type=int)
    per_page = request.get('per_page', 10, type=int)
    pagination = Order.query.paginate(
        page,
        per_page=per_page,
        error_out=False
    )
    orders = pagination.items
    prev_ = None
    if pagination.has_prev:
        prev_ = url_for('api.get_orders', shop_id=shop_id,
                        page=page-1, per_page=per_page)
    next_ = None
    if pagination.has_next:
        next_ = url_for('api.get_orders', shop_id=shop_id,
                        page=page+1, per_page=per_page)
    resp = {
        'orders': [order.to_json() for order in orders],
        'prev_url': prev_,
        'next_url': next_,
        'total': pagination.total
    }
    return klass_response.SuccessResult(resp, 200).to_json()


@api.route('/order/<int:order_id')
def get_order_by_id(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order').to_json()
    return klass_response.SuccessResult(order.to_json(), 200).to_json()


@api.route('/order/<int:order_id>', methods=['PUT'])
def _edit_order_by_id(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order').to_json()
    return klass_response.SuccessResult('Not Neccessary', 200).to_json()


@api.route('/order/<int:shop_id>', methods=['POST'])
def add_order(shop_id):
    """add a new order"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop').to_json()

    # generate a string for order_name
    order_name = bowl.Bowl.generate_time_str()
