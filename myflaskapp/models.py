from .database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # New field to store password hashes
    tweets = db.relationship('Tweet', backref='author', lazy=True)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    text = db.Column(db.String(140))
    # You may want to store the timestamp of the tweet
    timestamp = db.Column(db.DateTime, index=True)

    comments = db.relationship('Comment', backref='tweet', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    text = db.Column(db.String(140))
    # You may want to store the timestamp of the comment
    timestamp = db.Column(db.DateTime, index=True)
