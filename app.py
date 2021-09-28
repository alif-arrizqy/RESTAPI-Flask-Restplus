import json
from flask import request, jsonify, make_response
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
import jwt
from setting import *
from controller import user_controller
from model.user import *
from model.detail_user import *


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = Users.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorator

@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == 'GET':
        return jsonify({"user": user_controller.get_all_user()})
    else:
        return user_controller.create()


@app.route("/user/<id>", methods=["PUT", "GET", "DELETE"])
def user_detail(id):
    if request.method == 'GET':
        return user_controller.get_single_user(id)
    elif request.method == 'PUT':
        return user_controller.update(id)
    elif request.method == 'DELETE':
        return user_controller.delete(id)


# @app.route("/register", methods=["POST"])
# def signup_user():
#     data = request.get_json()
#     add_user(data["username"], data["password"], data["name"], data["status"])
#     return jsonify({"message": "registered successfully"})


@app.route("/login", methods=["POST"])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )

    user = Users.query.filter_by(username=auth.username).first()
    if user.status == 1:
        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
            )
            return jsonify({"token": token.decode("UTF-8")})
    else:
        return jsonify({"message": "login as user"})
    return make_response("Couldnt verify", 401)

# # User
# @app.route("/user", methods=["GET"])
# # @token_required
# def get_all_users():
#     return jsonify({"user": Users.get_all_user()})


# @app.route("/detail_user/<id>", methods=["POST"])
# @token_required
# def add_detail_user(current_user, id):
#     data = request.get_json()
#     success = DetailUsers.add_detail_user(
#         current_user.id, data["address"], data["phone_number"], data["email"]
#     )
#     return success if success else jsonify({"message": "Failed to added Detail User"})


# @app.route("/detail_user/<user_id>", methods=["GET"])
# @token_required
# def detail_user(current_user, user_id):
#     user_id = current_user.id
#     match = DetailUsers.get_detail_user(user_id)
#     return match if match else jsonify({"message": "Data User not Found 404"}, 404)


# @app.route("/user/<id>", methods=["DELETE"])
# @token_required
# def delete_user(current_user, id):
#     id = current_user.id
#     Users.delete_user(id)
#     return jsonify({"message": "User deleted"})


# Author
# @app.route("/authors", methods=["GET"])
# @token_required
# def get_authors(current_user):
#     return jsonify({"author": Authors.get_author()})


# @app.route("/authors", methods=["POST"])
# @token_required
# def add_author(current_user):
#     data = request.get_json()
#     Authors.add_author(
#         current_user.id,
#         data["author"],
#         data["phone_number"],
#         data["email"]
#     )
#     return jsonify({"message": "add author successfully"})

# @app.route("/authors/<author>/<book>", methods=["DELETE"])
# @token_required
# def delete_author(author, book):
#     Authors.delete_author(author, book)
#     return jsonify({"message": "Author deleted"})


# Book
# @app.route("/book/<author_id>/<title_book>", methods=["GET"])
# @token_required
# def get_book(current_user, author_id, title_book):
#     return jsonify({"book": Book.get_book()})

# @app.route("/book", methods=["POST"])
# @token_required
# def add_book(current_user):
#     data = request.get_json()
#     Book.add_book(
#         data["author_id"],
#         data["title_book"],
#         data["country"],
#         data["publisher"],
#         data["synopsis"],
#     )
#     return jsonify({"message": "add book successfully"})


# @app.before_first_request #Creates everything before the first request.
# def startup():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True)