"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Puzzle, Order
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # Change this!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config['JWT_SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def all_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    request_body_user = request.get_json()

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    if "full_name" in request_body_user:
        user1.full_name = request_body_user["full_name"]  
    if "email" in request_body_user:
        user1.email = request_body_user["email"]
    if "address" in request_body_user:
        user1.address = request_body_user["address"]
    if "city" in request_body_user:
        user1.city = request_body_user["city"] 
    if "state" in request_body_user:
        user1.state = request_body_user["state"]
    if "zip" in request_body_user:
        user1.zip = request_body_user["zip"]               
    if "username" in request_body_user:
        user1.username = request_body_user["username"]
    db.session.commit()

    return jsonify(request_body_user), 200  

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify("ok"), 200

@app.route('/order/<puzzle_id>', methods=['POST'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    return jsonify({'hello_from': get_jwt_identity()}), 200

#def order_product(puzzle_id):


#Register Endpoint
@app.route('/register', methods=['POST'])
def register():

    request_body_user = request.get_json()

    newuser = User(full_name=request_body_user["full_name"], email=request_body_user["email"], address=request_body_user["address"],
    city=request_body_user["city"], state=request_body_user["state"],
    zip=request_body_user["zip"], username=request_body_user["username"], password=request_body_user["password"])
    db.session.add(newuser)
    db.session.commit()

    return jsonify(request_body_user), 200  

#Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    userquery = User.query.filter_by(username = username).first()
    if userquery is None:
        return jsonify({"msg": "user not found"}), 401
    if userquery.validate_password(password) is False:
        return jsonify({"msg": "invalid password"}), 401

    
    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username), 'user': userquery.serialize()}
    return jsonify(ret), 200    

@app.route('/order', methods=['POST'])
def order_product():

    response_body = {
                "msg": "Hello, this is your ORDER /user response "
     }

    return jsonify("order complete"), 200

#this should send the post information to USPS 
#will need to use address + name + weight

@app.route('/puzzle', methods=['GET'])
def get_puzzle():

    all_puzzles = Puzzle.query.all()
    all_puzzles = list(map(lambda x: x.serialize(), all_puzzles))
    return jsonify(all_puzzles), 200

   

# @app.route('/puzzle', methods=['POST'])
# def create_puzzle():

#     response_body = {
#         "msg": "Puzzle upload endpoint"
#     }

#     return jsonify(response_body), 200

@app.route('/puzzle', methods=['POST'])
def create_puzzle():

    request_body_puzzle = request.get_json()

    newpuzzle = Puzzle(
    name_of_puzzle=request_body_puzzle["name_of_puzzle"], 
    picture_of_puzzle=bytes(request_body_puzzle["picture_of_puzzle"], 'utf-8'), 
    picture_of_box=bytes(request_body_puzzle["picture_of_box"], 'utf-8'), 
    number_of_pieces=request_body_puzzle["number_of_pieces"], 
    age_range=request_body_puzzle["age_range"], 
    category=request_body_puzzle["category"], 
    owner_id=request_body_puzzle["owner_id"],
    is_available=request_body_puzzle["is_available"]
    )
    db.session.add(newpuzzle)
    db.session.commit()

    return jsonify(request_body_puzzle), 200 

@app.route('/puzzle', methods=['PUT'])
def edit_puzzle():

    response_body = {
        "msg": "Puzzle user edit endpoint"
    }

    return jsonify(response_body), 200    

@app.route('/puzzle/<int:puzzle_id>', methods=['DELETE'])
def delete_puzzle(puzzle_id):

    user1 = User.query.get(puzzle_id)
    if puzzle1 is None:
        raise APIException('Puzzle not found', status_code=404)
    db.session.delete(puzzle1)
    db.session.commit()

    return jsonify("ok"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
