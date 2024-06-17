import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

## local database path
database_name = 'movie_child'
database_path = 'postgresql://{}/{}'.format('localhost:5432', database_name)

## environment database path
'''
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)
'''
db = SQLAlchemy()

#database_filename = "database.db"
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

#db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

"""
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
"""

## Test: setup_db(app): if want to use a test database

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    pred_rating = Pred_Rating(
        id = 1,
        type='G',
        note='appropriate for all ages'
    )
    pred_rating.insert()

    pred_rating = Pred_Rating(
        id = 2,
        type='PG',
        note='parental guidance is suggested'
    )
    pred_rating.insert()

    pred_rating = Pred_Rating(
        id = 3,
        type='PG-13',
        note='Parents strongly cautioned. Some material may be inappropriate for children under 13'
    )
    pred_rating.insert()

    pred_rating = Pred_Rating(
        id = 4,
        type='R',
        note='Under 17 requires accompanying parent or adult guardian'
    )
    pred_rating.insert()

    pred_rating = Pred_Rating(
        id = 5,
        type='NC-17',
        note='No One 17 and Under Admitted'
    )
    pred_rating.insert()

    movie = Movie(
        title='test1',
        year = 1990,
        duration = 120,
        pred_rating_id = 1,
        detail='[{"director": "AA", "writer": "a1, b1", "Cast": "a2, b2"}]'
    )
    movie.insert()

    movie = Movie(
        title='test2',
        year = 1999,
        duration = 200,
        pred_rating_id = 2,
        detail='[{"director": "CC", "writer": "c1, d1", "Cast": "c2, c2"}]'
    )
    movie.insert()
# ROUTES

'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Movie(db.Model):
    __tablename__ = 'Movie'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    year = Column(Integer,nullable=False)
    duration = Column(Integer,nullable=False)
    pred_rating_id = Column(Integer, db.ForeignKey('Pred_Rating.id'), nullable=False)
    pred_rating = db.relationship('Pred_Rating', backref='movie', lazy=True)
    detail = Column(String(180), nullable=False)


    def __init__(self, title, year, duration,detail,pred_rating_id):
        self.title = title
        self.year = year
        self.duration = duration
        self.pred_rating_id  = pred_rating_id 
        self.detail = detail
    
    def short_format(self):
        return {
            'title': self.title,
            'year': self.year,
            'duration': self.duration,
            'pred_rating_id': self.pred_rating_id,
            'pred_rating': self.pred_rating.type
            }
    
    def long_format(self):
        return {
            'title': self.title,
            'year': self.year,
            'duration': self.duration,
            'pred_rating_id': self.pred_rating_id,
            'pred_rating': self.pred_rating.type,
            'pred_rating_note': self.pred_rating.note,
            'detail': json.loads(self.detail)
            }

    def short(self):
        #print(json.loads(self.detail))
        short_detail = [{'director': d['director'], 'writer': d['writer']} for d in json.loads(self.detail)]
        return {
            'id': self.id,
            'title': self.title,
            'duration': self.duration,
            'pred_rating_id': self.pred_rating_id,
            'pred_rating': self.pred_rating.type,
            'detail': short_detail
        }

    
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'duration': self.duration,
            'pred_rating_id': self.pred_rating_id,
            'pred_rating': self.pred_rating.type,
            'pred_rating_note': self.pred_rating.note,
            'detail': json.loads(self.detail)
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Pred_Rating(db.Model):
    __tablename__ = 'Pred_Rating'
    ## G,PG,PG-13,R,NC-17

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    type = Column(String)
    note = Column(String)

    
    def __init__(self, id,type,note):
        self.type = 1
        self.type = type
        self.note = note


    ## define revisions for show model:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    ## define show_template for show model
    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'note': self.note
            }

    def __repr__(self):
        return json.dumps(self.format())