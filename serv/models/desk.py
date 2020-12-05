# coding utf-8

"""
filename: desk.py
author: 1000px
time: 2020-10-16
desc: desk's model
| property  | type    | desc                                        |
|-----------+---------+---------------------------------------------|
| id        | int     | the primary                                 |
| desk_size | int     | the count of this desk's seats              |
| disabled  | boolean | the desk is or not usable                   |
| shop_id   | int     | the desk belongs to the shop                |
| order     | int     | desk's order                                |
| room      | int     | you can contain the desks by different room |
"""
from serv import db


class Desk(db.Model):
    """Desk Model"""
    __tablename__ = 'desks'
    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    desk_size = db.Column(db.Integer, default=0)
    desk_num = db.Column(db.Integer, default=1)
    disabled = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=1) # 顺序
    room = db.Column(db.Integer, default=1) # 房间
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))

    def __init__(self, desk_num, shop_id, desk_size=6, room=1, order=1):
        self.desk_num = desk_num
        self.shop_id = shop_id
        self.desk_size = desk_size
        self.room = room
        self.order = order

    def to_json(self):
        """return desk json's object"""
        return {
            'id': self.id,
            'desk_size': self.desk_size,
            'desk_num': self.desk_num,
            'disabled': self.disabled,
            'order': self.order,
            'room': self.room,
            'shop_id': self.shop_id
        }
