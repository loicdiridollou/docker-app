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

    ## Actor routes

    @app.route('/actors', methods=['GET'])
    def list_actors():
        actors = [actor.format() for actor in Actor.query.all()]
        return jsonify({"success": True, "actors": actors}), 200

    @app.route('/actors', methods=['POST'])
    def add_actor():
        body = request.get_json()

        if body is None:
            return abort(400)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()

        return jsonify({'success': True,
                        'created': new_actor.id})

    @app.route('/actors/<actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        body = request.get_json()

        if actor is None or body is None:
            abort(400)

        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender

        actor.update()

        return jsonify({'success': True,
                        'actor updated': actor_id}), 200

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    def delete_actors(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(400)

        actor.delete()

        return jsonify({'success': True,
                        'actor deleted': actor_id}), 200

    ## Movie routes

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

    @app.errorhandler(400)
    def bet_request(error): # pylint: disable=unused-argument
        return jsonify({'success': False,
                        'error': 400,
                        'message': 'bad request'
                        }), 400



    return app


app = create_app()
