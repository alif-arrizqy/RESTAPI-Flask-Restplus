from flask import jsonify, request
import json
from model.user import *


def add_detail_user(id):
    _user_id = id
    _address = request.json["address"]
    _phone_number = request.json["phone_number"]
    _email = request.json["email"]

    detail_user = DetailUsers(
        user_id=_user_id,
        address=_address,
        phone_number=_phone_number,
        email=_email,
    )
    db.session.add(detail_user)
    db.session.commit()
    return jsonify({"message": "User details added successfully"})

def singleTransform(details):
    data = {
        'address': details.address,
        'phone_number': details.phone_number,
        'email': details.email,
    }
    return data