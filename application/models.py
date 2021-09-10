# application/models.py
import os # pylint: disable=unused-import
from datetime import date
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy


DATABASE_PATH = 'postgresql://rlrkfvwqfrqqnt:095a3fbe34d7a5eee144d8c74f909b1079dd521c2bdc0edb5ecd4178dd03ac5b@ec2-54-147-126-173.compute-1.amazonaws.com:5432/d8g32a2871o87o' # pylint: disable=line-too-long
#os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')

db = SQLAlchemy()

def db_setup(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print(app.config["SQLALCHEMY_DATABASE_URI"][:10])
    db.app = app
    db.init_app(app)
    db.create_all()

def db_reset():
    db.drop_all()
    db.create_all()
    db_populate()

def db_populate():
    new_actor = (Actor(
        name = 'Anne',
        gender = 'Female',
        age = 23
        ))

    new_movie = (Movie(
        title = 'Anne first Movie',
        release_date = date.today()
        ))

    new_actor.insert()
    new_movie.insert()
    db.session.commit()


########################################
# Actors model
# id, name, gender, age
########################################

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name' : self.name,
        'gender': self.gender,
        'age': self.age
        }


########################################
# Movies model
# id, title, release_date, actors
########################################

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = Column(String)

    def __init__(self, title, release_date) :
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'title' : self.title,
        'release_date': self.release_date
        }
