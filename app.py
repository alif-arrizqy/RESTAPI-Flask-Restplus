from flask import request, jsonify, make_response
from setting import *
from userModel import *

def token_required(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        token = None 
        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens'] 

        if not token:  
            return jsonify({'message': 'a valid token is missing'}), 401

        try:  
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = Users.query.filter_by(public_id=data['public_id']).first()  
        except:  
            return jsonify({'message': 'token is invalid'}), 401 
        
        return f(current_user, *args,  **kwargs)  
    return decorator 


@app.route('/register', methods=['POST'])
def post_signup_user():  
    data = request.get_json()
    Users.signup_user(data["name"], data["password"])

    return jsonify({'message': 'registered successfully'})


@app.route("/login", methods=["POST"])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"public_id": user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])
        return jsonify({"token": token.decode("UTF-8")})
    
    return make_response("Couldnt verify", 401)


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    return jsonify({"user": Users.get_all_user()})

@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    id = current_user.id
    Users.delete_user(id)

    return jsonify({'message': 'User deleted'})


# Author
@app.route('/authors', methods=['GET'])
@token_required
def get_authors(current_user):
    return jsonify({"author": Authors.get_author()})


@app.route('/authors', methods=['POST'])
@token_required
def add_author(current_user):
    data = request.get_json()
    Authors.add_author(
        data["name"],
        data["book"],
        data["country"],
        True,
        current_user.id

    )
    
    return jsonify({'message': 'add author successfully'}) 


@app.route('/authors/<name>', methods=['DELETE'])
@token_required
def delete_author(current_user, name):
    user_id = current_user.id
    Authors.delete_author(user_id, name)
    
    return jsonify({'message': 'Author deleted'})


if  __name__ == '__main__':  
    app.run(debug=True) 