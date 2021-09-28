from flask import jsonify, request
import json
import uuid
from werkzeug.security import generate_password_hash
from model.user import *
# from model.detail_user import *
from controller import detail_user_controller


def add_user():
    _username = request.json["username"]
    _password = request.json["password"]
    _name = request.json["name"]
    _status = request.json["status"]
    
    hashed_password = generate_password_hash(password=_password, method="sha256")
    new_user = Users(
        # public_id=str(uuid.uuid4()),
        username=_username,
        password=hashed_password,
        name=_name,
        status=_status,
    )
    db.session.add(new_user)

    # detail user
    _address = request.json["address"]
    _phone_number = request.json["phone_number"]
    _email = request.json["email"]

    detail_user = DetailUsers(
        address=_address,
        phone_number=_phone_number,
        email=_email,
        users=new_user #user_id
    )
    db.session.add(detail_user)
    db.session.commit()
    return jsonify({"message": "registered successfully"})


def get_all_user():
    return [Users.json(user) for user in Users.query.all()]


def get_single_user(_id):
    data = Users.query.filter_by(id=_id).first()
    get_data = singleTransform(data)
    return get_data

def singleTransform(values):
    data = {
        'id': values.id,
        'username': values.username,
        'name': values.name,
        'status': values.status,
        # 'created_on': values.created_on,
        'detail': detail_user_controller.singleTransform(values.get_detail)
    }
    return data

# def delete_user(_id):
#     Users.query.filter_by(id=_id).delete()
#     db.session.commit()
