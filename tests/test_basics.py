# coding utf-8

"""
basic test file
test the config of aos app instance
"""
import unittest
from flask import current_app
# pylint: disable=import-error
from serv import create_app, db


class BasicsTestCase(unittest.TestCase):
    """Basics Test Case"""
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """test app instance is exist or not"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """test app is testing or not"""
        self.assertTrue(current_app.config['TESTING'])
