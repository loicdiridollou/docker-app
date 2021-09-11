# application/__init__.py
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from application.models import db_reset, db_setup, Actor, Movie


def create_app(test_config=None):
    """Creating the app and db
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')
    db_setup(app)

    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def home():
        return jsonify({'message': 'healthy'}), 200

    @app.route('/actors')
    def list_actors():
        actors = [actor.format() for actor in Actor.query.all()]
        return jsonify({"success": True, "actors": actors}), 200

    @app.route('/movies')
    def list_movies():
        movies = [movie.format() for movie in Movie.query.all()]
        return jsonify({"success": True, "movies": movies}), 200



    @app.errorhandler(404)
    def not_found(error): # pylint: disable=unused-argument
        return jsonify({'success': False,
                        'error': 404,
                        'message': 'resource not found'
                        }), 404


    return app


app = create_app()
