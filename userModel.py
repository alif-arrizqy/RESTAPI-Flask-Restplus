from flask import jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from setting import *

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def json(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "name": self.name,
            "admin": self.admin,
        }

    def signup_user(_name, _password):
        hashed_password = generate_password_hash(password=_password, method="sha256")

        new_user = Users(
            public_id=str(uuid.uuid4()),
            name=_name,
            password=hashed_password,
            admin=False,
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "registered successfully"})

    def get_all_user():
        return [Users.json(user) for user in Users.query.all()]

    def delete_user(_id):
        delete_user = Users.query.filter_by(id=_id).first()
        db.session.delete(delete_user)
        db.session.commit()

    def __repr__(self):
        user_object = {
            "id": self.id,
            "public_id": self.public_id,
            "name": self.name,
            "admin": self.admin,
        }
        return json.dumps(user_object)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    book = db.Column(db.String(20), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    booker_prize = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def json(self):
        return {
            "name": self.name,
            "book": self.book,
            "country": self.country,
            "book_prize": self.booker_prize,
            "user_id": self.user_id,
        }

    def get_author():
        return [Authors.json(author) for author in Authors.query.all()]

    def add_author(_name, _book, _country, _booker_prize, _user_id):
        new_author = Authors(
            name=_name,
            book=_book,
            country=_country,
            booker_prize=_booker_prize,
            user_id=_user_id,
        )
        db.session.add(new_author)
        db.session.commit()

    def delete_author(_user_id, _name):
        delete_author = Authors.query.filter_by(name=_name, user_id=_user_id).first()
        db.session.delete(delete_author)
        db.session.commit()

    def __repr__(self):
        author_object = {
            "name": self.name,
            "book": self.book,
            "country": self.country,
            "book_prize": self.booker_prize,
            "user_id": self.user_id,
        }
        return json.dumps(author_object)
