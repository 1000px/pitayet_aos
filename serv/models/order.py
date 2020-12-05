# coding utf-8

"""
order's model file

| property     | type  | desc                                             |
|--------------+-------+--------------------------------------------------|
| id           | int   | the primary key                                  |
| order_name   | str   | a long char list,must unique                     |
| start_time   | date  | order start                                      |
| end_time     | date  | order end                                        |
| order_price  | float |                                                  |
| order_detail | list  | eg:'[id] [count] [price];[id2] [count] [price2]' |
"""
from datetime import datetime
from serv import db
from .dish import Dish
from .desk import Desk
import hashlib
import time


class Order(db.Model):
    """Order Model"""
    __tablename__ = 'orders'

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(256), unique=True, index=True)
    start_time = db.Column(db.DateTime(), default=datetime.utcnow)
    end_time = db.Column(db.DateTime())
    order_price = db.Column(db.Float)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    desk_id = db.Column(db.Integer)
    # [id] [count] [price_single];[id] [count] [price_single];
    order_detail = db.Column(db.Text())
    
    def __init__(self, order_price, desk_id, shop_id=1):
        time_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
        m = hashlib.md5()
        m.update(time_str.encode('utf-8'))

        self.order_name =  time_str + '-' + m.hexdigest()
        self.order_price = order_price
        self.desk_id = desk_id
        self.shop_id = shop_id


    @property
    def dishes(self):
        """readable property"""
        # str to list
        if self.order_detail is None:
            return None
        return [{'dish': Dish.query.filter_by(id=int(dish.split(' ')[0])).first().to_json(),
                'count': int(dish.split(' ')[1])}
                for dish in self.order_detail.split(';')]

    @dishes.setter
    def dishes(self, dishes):
        self.order_detail = ';'.join([' '.join(dish) for dish in dishes])

    def to_json(self):
        """return json object"""
        return {
            'order_name': self.order_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'order_price': self.order_price,
            'desk': Desk.query.filter_by(id=self.desk_id).first().to_json(),
            'dishes': self.dishes
        }
