# coding utf-8

"""
user's model
| property      | type    | desc                         |
|---------------+---------+------------------------------|
| id            | int     | the primary keys             |
| user_name      | str     | the user's name              |
| email         | str     | not null                     |
| password_hash | str     | hash string                  |
| role          | int     |                              |
| disabled      | boolean | default false                |
| shops         | list    | one user can buy a few shops |
"""
# pylint: disable=import-error
from serv import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model):
    """user's model"""
    __tablename__ = 'users'

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.Integer, default=0)
    disabled = db.Column(db.Boolean, default=False)

    shops = db.relationship('Shop', backref='user')

    @property
    def password(self):
        """the password property is not readable"""
        raise AttributeError('password is not readable property.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """verify password"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        """generate auth token"""
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        """User class static method for verifying auth token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        """return json object"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'disabled': self.disabled
        }
