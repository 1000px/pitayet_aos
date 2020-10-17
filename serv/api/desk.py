# coding utf-8

"""
filename: desk.py
author: 1000px
time: 2020-10-16
desc: desk's api list
| Function Name            | Entry Params | Out Params     | Desc                             |
|--------------------------+--------------+----------------+----------------------------------|
| get_desks                | shop_id      | Json format CR | desks                            |
| update_desks             | shop_id      | same up        | change desks infor,eg:room,order |
| toggle_status_by_desk_id | desk_id      | same up        | disabled or not                  |
| add_desks                | shop_id      | same up        | add a few desks                  |
| del_desk_by_id           | desk_id      | same up        | delete                           |

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
from serv.models import Desk, Shop
from serv.api import api
from flask import request, url_for
from serv.utils import klass_response
from sqlalchemy.exc import IntegrityError


@api.route('/desks/<int:shop_id>')
def get_desks(shop_id):
    """get desks"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    desks = Desk.query.filter_by(shop_id=shop_id).all()
    if len(desks) == 0:
        return klass_response.FailedResult('not_exist', 'Desks')
    data_obj = {
        'desks': [desk.to_json() for desk in desks],
        'total': desks.count
    }
    return klass_response.SuccessResult(data_obj, 200)


@api.route('/desks/<int:shop_id>', methods=['POST'])
def add_desks(shop_id):
    """add desks"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    desks = request.json.get('desks')
    if len(desks) <= 0:
        return klass_response.FailedResult('params_err', 'desks')
    for desk_ in desks:
        desk = Desk()
        if desk_['desk_size'] is not None:
            desk.desk_size = desk_['desk_size']
        if desk_['desk_num'] is not None:
            desk.desk_num = desk_['desk_num']
        if desk_['order'] is not None:
            desk.order = desk_['order']
        if desk_['room'] is not None:
            desk.room = desk_['room']
        # pylint: disable=no-member
        db.session.add(desk)
    try:
        # pylint: disable=no-member
        db.session.commit()
    except IntegrityError:
        # pylint: disable=no-member
        db.rollback()
        return klass_response.FailedResult('params_err', 'desks inner')

    return klass_response.SuccessResult(None, 200)


@api.route('/desks/<int:shop_id>', methods=['PUT'])
def update_desks(shop_id):
    """update desks"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        return klass_response.FailedResult('not_exist', 'Shop')
    desks = request.json.get('desks')
    if len(desks) <= 0:
        return klass_response.FailedResult('params_err', 'desks')
    for desk_ in desks:
        if desk_['id'] is None:
            return klass_response.FailedResult('params_err', 'Key: id')
        desk = Desk.query.filter_by(id=desk_['id']).first()
        if desk is None:
            return klass_response.FailedResult('not_exist', 'Desk')
        if desk_['desk_size'] is not None:
            desk.desk_size = desk_['desk_size']
        if desk_['desk_num'] is not None:
            desk.desk_num = desk_['desk_num']
        if desk_['order'] is not None:
            desk.order = desk_['order']
        if desk_['room'] is not None:
            desk.room = desk_['room']
        # pylint: disable=no-member
        db.session.add(desk)
    try:
        # pylint: disable=no-member
        db.session.commit()
    except IntegrityError:
        # pylint: disable=no-member
        db.rollback()
        return klass_response.FailedResult('params_err', 'desks inner')

    return klass_response.SuccessResult(None, 200)


@api.route('/desk/status/<int:desk_id>', methods=['PUT'])
def toggle_status_by_desk_id(desk_id):
    """toggle desk's status: disabled or not"""
    desk = Desk.query.filter_by(id=desk_id).first()
    if desk is None:
        return klass_response.FailedResult('not_exist', 'Desk')
    desk.disabled = not desk.disabled
    # pylint: disable=no-member
    db.session.add(desk)
    db.session.commit()
    return klass_response.SuccessResult(desk.to_json(), 200)


@api.route('/desk/<int:desk_id>', methods=['DELETE'])
def del_desk_by_id(desk_id):
    desk = Desk.query.filter_by(id=desk_id).first()
    if desk is None:
        return klass_response.FailedResult('not_exist', 'Desk')
    # pylint: disable=no-member
    db.session.delete(desk)
    db.session.commit()
    return klass_response.SuccessResult(None, 200)
