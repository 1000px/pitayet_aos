# coding utf-8

"""
The project entry
You can run this server at this
"""
import os
import click
from serv import create_app, db
from serv.models import User, Shop, Dish, Category


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """When you run the shell from flask, you can use this context."""
    return dict(
        db=db,
        User=User,
        Shop=Shop,
        Dish=Dish,
        Category=Category
    )


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    discover_ = unittest.TestLoader().discover('tests', pattern='test*.py')
    suite = unittest.TestSuite()
    suite.addTest(discover_)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
