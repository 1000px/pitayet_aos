# coding: utf-8
"""
This is the config for the pitayet_aos app
There are 3 config class:
DevConfig
TestConfig
ProductionConfig
"""
import os


basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    """All the project's default config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'a good string that is hard to guess'
    RES_IMG = os.environ.get('RES_IMG')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    """special config for dev env"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestConfig(Config):
    """special config for test env"""
    SQLALCHEMY_DATA_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    """special config for production env"""
    SQLALCHEMY_DATA_URI = os.environ.get('PRODUCTION_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-production.sqlite')


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
