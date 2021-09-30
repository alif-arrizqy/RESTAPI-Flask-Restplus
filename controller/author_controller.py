from flask import jsonify, request
from model.models import *


def create(_id):
    """
    create author
    """
    data = Users.query.filter_by(id=_id).first()
    if not data:
        return jsonify({"message": "ID is not found"}), 401
    
    _author_name = request.json["author_name"]
    _email = request.json["email"]
    _user_id = data.id

    new_author = Author(
        author_name=_author_name,
        email=_email,
        user_id=_user_id
    )
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"message": "author successfully added"})


def get_all_author():
    """
    Return all author
    """
    return [Author.json(author) for author in Author.query.all()]


def get_single_author(_id):
    """
    Return single author
    """
    data = Author.query.filter_by(id=_id).first()
    if not data:
        return jsonify({"message": "ID is not found"}), 401

    get_data = singleTransform(data)
    return jsonify({"author": get_data})


def singleTransform(values):
    """
    Get data from Author
    """
    data = {
        "id": values.id,
        "name_author": values.author_name,
        "email": values.email,
        "created_by": createdBy(values.users)
    }
    return data


def createdBy(datas):
    data = {
        "name": datas.name
    }
    return data
