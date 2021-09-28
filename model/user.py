from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from setting import *
import json

db = SQLAlchemy(app)

class Users(db.Model):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    status = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    get_detail = db.relationship('DetailUsers', backref='users', uselist=False)

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "status": self.status,
            "created_on": self.created_on,
        }


    def __repr__(self):
        user_object = {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "status": self.status,
            "created_on": self.created_on,
        }
        return json.dumps(user_object)

class DetailUsers(db.Model):
    # __tablename__ = "detail_user"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # get_user = db.relationship("Users", backref="user_id")

    def json(self):
        return {
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }


    def __repr__(self):
        detail_object = {
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }
        return json.dumps(detail_object)
    