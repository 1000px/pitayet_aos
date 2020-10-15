# coding utf-8

"""
category's model
| property      | type | desc                      |
|---------------+------+---------------------------|
| id            | int  | the primary key           |
| category_name | str  | the category's name       |
| order         | int  | order the category        |
| shop_id       | int  | the shop of this category |
"""
# pylint: disable=import-error
from serv import db
from serv.models.shop import Shop


class Category(db.Model):
    """category's model"""
    __tablename__ = 'categories'

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(256), unique=True, index=True)
    order = db.Column(db.Integer, default=0)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))

    # pylint: disable=unused-argument
    def __init__(self, category_name):
        """init Category instance"""
        self.category_name = category_name

    def to_json(self):
        """return json object of Category instance"""
        return {
            'id': self.id,
            'category_name': self.category_name,
            'order': self.order,
            'shop_id': self.shop_id
        }
