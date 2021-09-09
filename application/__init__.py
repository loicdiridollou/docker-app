# application/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    """Creating the app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def home():
        return 'Hello World!'

    return app



app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)