from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache


db = SQLAlchemy()
cache = Cache()

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    votes = db.Column(db.Integer, default=0)


