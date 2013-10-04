from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(64))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))