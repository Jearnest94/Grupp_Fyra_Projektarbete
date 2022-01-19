import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    mangocount = db.Column(db.Integer, default=0)
    admin = db.Column(db.BOOLEAN, default=False)


class Message(db.Model):
    messageid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fromuser = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    touser = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50))
    content = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
