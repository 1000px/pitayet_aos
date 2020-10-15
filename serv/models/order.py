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
    # [id] [count] [price_single];[id] [count] [price_single];
    order_detail = db.Column(db.Text())

    @property
    def dishes(self):
        """readable property"""
        # str to list
        return [dish.split() for dish in self.order_detail.split(';')]

    @dishes.setter
    def dishes(self, dishes):
        self.detail = ';'.join([''.join(dish) for dish in dishes])

    def to_json(self):
        """return json object"""
        return {
            'order_name': self.order_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'order_price': self.order_price,
            'dishes': self.dishes
        }
