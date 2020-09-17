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
from models import db, User
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

@app.route('/user', methods=['POST'])
def create_user():

    request_body_user = request.get_json()

    newuser = User(full_name=request_body_user["full_name"], address=request_body_user["address"], city=request_body_user["city"], state=request_body_user["state"], zip_code=request_body_user["zip_code"], email=request_body_user["email"], username=request_body_user["username"], password=request_body_user["password"])
    db.session.add(newuser)
    db.session.commit()

    return jsonify(request_body_user), 200  


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    request_body_user = request.get_json()

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    if "full_name" in request_body_user:
        user1.full_name = request_body_user["full_name"]
    if "address" in request_body_user:
        user1.address = request_body_user["address"]
    if "city" in request_body_user:
        user1.city = request_body_user["city"] 
    if "state" in request_body_user:
        user1.state = request_body_user["state"]               
    if "zip_code" in request_body_user:
        user1.zip_code = request_body_user["zip_code"]    
    if "email" in request_body_user:
        user1.email = request_body_user["email"]
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
#def protected():
    # Access the identity of the current user with get_jwt_identity
    #return jsonify({'hello_from': get_jwt_identity()}), 200
def order_product(puzzle_id):

    response_body = {
                "msg": "Hello, this is your ORDER /user response "
     }

    return jsonify("order complete"), 200

#this should send the post information to USPS 
#will need to use address + name + weight

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
