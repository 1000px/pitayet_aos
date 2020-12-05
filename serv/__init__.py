# coding utf-8

"""
the module of creating a flask instance
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config_name):
    """You can create a app instance by using this function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from serv.api import api as api_blueprint
    CORS(api_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # pylint: disable=unused-variable
    migrate = Migrate(app, db)

    return app
