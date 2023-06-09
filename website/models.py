from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    #setup one to many relationship
    posts = db.relationship('Post', backref='user', passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    tag1 = db.Column(db.String(32))
    tag2 = db.Column(db.String(32))
    tag3 = db.Column(db.String(32))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    is_private = db.Column(db.Integer, default = 0)
    #sets up one to many relationship with foreignkey
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


