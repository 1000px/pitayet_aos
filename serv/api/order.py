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
from serv.utils import klass_response, bowl
from flask import request, url_for, jsonify
from serv.models.order import Order
from serv.models.shop import Shop
from datetime import datetime


@api.route('/orders/<int:shop_id>')
def get_orders(shop_id):
    """get order list by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
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
    return klass_response.SuccessResult(resp, 200)


@api.route('/order/<int:order_id>')
def get_order_by_id(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order')
    return klass_response.SuccessResult(order.to_json(), 200)


@api.route('/order/<int:order_id>', methods=['PUT'])
def _edit_order_by_id(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order')
    return klass_response.SuccessResult('Not Neccessary', 200)


@api.route('/order/<int:shop_id>', methods=['POST'])
def add_order(shop_id):
    """add a new order"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')

    dishes = request.json.get('dishes')
    print('add a new order...', dishes)
    order_price = request.json.get('order_price')

    # generate a string for order_name
    order = Order()
    order.order_name = bowl.Bowl.generate_time_str()
    order.shop_id = shop_id
    order.order_price = order_price
    order.dishes = [(str(dish['id']), str(dish['count'])) for dish in dishes]

    # pylint: disable=no-member
    db.session.add(order)
    db.session.commit()
    return klass_response.SuccessResult(order.to_json(), 200)


@api.route('/order/close/<int:order_id>', methods=['PUT'])
def close_order_by_id(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order')
    if order.end_time is not None:
        return klass_response.FailedResult('params_err',
                                           'The Order is already closed.')
    order.end_time = datetime.utcnow()
    # pylint: disable=no-member
    db.session.add(order)
    db.session.commit()
    return klass_response.SuccessResult(order.to_json(), 200)


@api.route('/order/<int:order_id>', methods=['DELETE'])
def del_order_by_id(order_id):
    """delete order by it's id"""
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order')
    # pylint: disable=no-member
    db.session.delete(order)
    db.session.commit()
    return klass_response.SuccessResult(None, 200)


@api.route('/order/update/<int:order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    """update order's dishes by it's id"""
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return klass_response.FailedResult('not_exist', 'Order')
    if order.end_time is not None:
        return klass_response.FailedResult('params_err',
                                           'this order already closed')
    dishes = request.json.get('dishes')
    if dishes is None or len(dishes) == 0:
        return klass_response.FailedResult('params_err',
                                           'dishes params must be array')

    order.dishes = [(str(dish['id']), str(dish['count'])) for dish in dishes]
    # pylint: disable=no-member
    db.session.add(order)
    db.session.commit()
    return klass_response.SuccessResult(order, 200)
