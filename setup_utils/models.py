from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
cache = Cache()
login_manager = LoginManager()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    votes = db.Column(db.Integer, default=0)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
