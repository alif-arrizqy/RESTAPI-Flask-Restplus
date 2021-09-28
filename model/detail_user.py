from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from setting import *
from model.user import Users
import json

db = SQLAlchemy(app)

class DetailUsers(db.Model):
    __tablename__ = "detail_user"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(Users.id))
    address = db.Column(db.Text())
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # get_user = db.relationship("Users", backref="user_id")

    def json(self):
        return {
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
        }


    def __repr__(self):
        detail_object = {
            "address": self.address,
            "phone_number": self.phone_number,
            "email": self.email,
        }
        return json.dumps(detail_object)