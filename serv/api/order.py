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
from serv.utils import klass_response
from flask import request, url_for
from serv.models.order import Order
from serv.models.shop import Shop


@api.route('/orders/<int:shop_id>')
def get_orders(shop_id):
    """get order list by shop's id"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
