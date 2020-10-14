# coding utf-8

"""
shop's model
| property | type | desc                         |
|----------+------+------------------------------|
| id       | int  | the primary key              |
| shop_name | str  | the shop's name              |
| dishes   | list | the dish's list of this shop |
| shop_img | str  | img uri of shop              |
| owner_id | int  | the shop's owner             |
"""
# pylint: disable=import-error
from serv import db


class Shop(db.Model):
    """shop's model"""
    __tablename__ = 'shops'

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(512), unique=True, index=True)
    shop_img = db.Column(db.String(256))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dishes = db.relationship('Dish', backref='Shop')

    def to_json(self):
        """return json object of the Shop instance"""
        return {
            'id': self.id,
            'shop_name': self.shop_name,
            'shop_img': self.shop_img,
            'owner_id': self.owner_id,
            'dishes': [dish.to_json() for dish in self.dishes]
        }
