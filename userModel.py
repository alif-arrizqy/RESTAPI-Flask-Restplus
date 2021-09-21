from enum import unique
from flask import jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime

from setting import *

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    status = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    # updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)    


    def json(self):
        return {
            "public_id": self.public_id,
            "username": self.username,
            "name": self.name,
            "status": self.status,
            "created_on": self.created_on,
            # "updated_on": self.updated_on,
        }

    def signup_user(_username, _password, _name, _status):
        hashed_password = generate_password_hash(password=_password, method="sha256")

        new_user = Users(
            public_id=str(uuid.uuid4()),
            username=_username,
            password=hashed_password,
            name=_name,
            status=_status,
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "registered successfully"})

    def get_all_user():
        return [Users.json(user) for user in Users.query.all()]

    def delete_user(_id):
        Users.query.filter_by(id=_id).delete()
        db.session.commit()

    def __repr__(self):
        user_object = {
            "public_id": self.public_id,
            "username": self.username,
            "name": self.name,
            "status": self.status,
            "created_on": self.created_on,
            # "updated_on": self.updated_on,
        }
        return json.dumps(user_object)


class Authors(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    synopsis = db.Column(db.Text(), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow) 


    def json(self):
        return {
            "book": self.book,
            "author": self.author,
            "publisher": self.publisher,
            "country": self.country,
            "synopsis": self.synopsis,
            "created_on": self.created_on,
        }

    def get_author():
        return [Authors.json(author) for author in Authors.query.all()]

    def add_author(_author, _book, _country, _publisher, _synopsis):
        new_author = Authors(
            author=_author,
            book=_book,
            country=_country,
            publisher=_publisher,
            synopsis=_synopsis,
        )
        db.session.add(new_author)
        db.session.commit()

    def delete_author(_book, _author):
        Authors.query.filter_by(author=_author, book=_book).delete()
        db.session.commit()
        

    def __repr__(self):
        author_object = {
            "author": self.author,
            "book": self.book,
            "country": self.country,
            "publisher": self.publisher,
            "synopsis": self.synopsis,
            "created_on": self.created_on,
        }
        return json.dumps(author_object)
