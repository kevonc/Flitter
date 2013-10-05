from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(64), unique = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __init__(self, fullname, username, password):
      self.fullname = fullname.title()
      self.username = username.lower()
      self.set_password(password)

    def set_password(self, password):
      self.password = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))