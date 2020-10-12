# coding utf-8

"""
The project entry
You can run this server at this
"""
import os
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
