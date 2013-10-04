from app import db

from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    pwdhash = db.Column(db.String(64))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self, fullname, email, password):
      self.fullname = fullname.title()
      self.email = email.lower()
      self.set_password(password)

    def set_password(self, password):
      self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.pwdhash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))