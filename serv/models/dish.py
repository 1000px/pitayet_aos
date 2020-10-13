# coding utf-8

"""
dish's model
| property    | type    | desc                      |
|-------------+---------+---------------------------|
| id          | int     | the primary key           |
| dish_name    | str     | the dish's name           |
| dish_desc   | str     | description of dish       |
| dish_img    | str     | img uri of dish           |
| shop_id     | int     | the shop of this dish     |
| hot         | boolean | default false             |
| category_id | int     | the category of this dish |
"""
# pylint: disable=import-error
from serv import db


class Dish(db.Model):
    """dish's model"""
    __tablename__ = 'dishes'
    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(256), unique=True, index=True)
    dish_desc = db.Column(db.Text())
    dish_img = db.Column(db.String(256))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    hot = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def to_json(self):
        """return json object of Dish instance"""
        return {
            'id': self.id,
            'dish_name': self.dish_name,
            'dish_desc': self.dish_desc,
            'dish_img': self.dish_img,
            'shop': self.shop_id,
            'hot': self.hot,
            'category': self.category_id
        }
