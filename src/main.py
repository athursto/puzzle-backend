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
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
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

@app.route('/user/<int:user_id>', methods=['GET'])
def get_address(user_id):

    # request_body_user = request.get_json()

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    # if "full_name" in request_body_user:
    #     user1.full_name = request_body_user["full_name"]  
    # if "address" in request_body_user:
    #     user1.address = request_body_user["address"]
    # if "city" in request_body_user:
    #     user1.city = request_body_user["city"] 
    # if "state" in request_body_user:
    #     user1.state = request_body_user["state"]
    # if "zip" in request_body_user:
    #     user1.zip = request_body_user["zip"]               

    # db.session.commit()

    return jsonify(user1.serialize()), 200      

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


@app.route('/order', methods=['GET'])

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


@app.route('/puzzle', methods=['POST'])
def create_puzzle():
# Get fields from Form Data
    name_of_puzzle = request.form["name_of_puzzle"] 
    picture_of_puzzle = request.files["picture_of_puzzle"] 
    picture_of_box = request.files["picture_of_box"]
    number_of_pieces = request.form["number_of_pieces"]
    age_range = request.form["age_range"]
    category = request.form["category"]
    owner_id = request.form["owner_id"]


    if picture_of_box is not None:
        # upload box to cloudinary
        box_upload_result = cloudinary.uploader.upload( picture_of_box )
    else:
        return jsonify("Failed to upload picture of box"), 500 

    if picture_of_puzzle is not None:
        # upload puzzle to cloudinary
        puzzle_upload_result = cloudinary.uploader.upload( picture_of_puzzle )
    else:
        return jsonify("Failed to upload picture of puzzle"), 500 

    # add to db
    

    request_body_puzzle = request.get_json()

    newpuzzle = Puzzle(
        name_of_puzzle=name_of_puzzle, 
        picture_of_puzzle=puzzle_upload_result['secure_url'], 
        picture_of_box=box_upload_result['secure_url'], 
        number_of_pieces=number_of_pieces, 
        age_range=age_range, 
        category=category, 
        owner_id=owner_id,
        is_available=True
    )
    db.session.add(newpuzzle)
    db.session.commit()

    return jsonify("successfully added puzzle"), 200 

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

#   @app.route('/payment', methods=['POST'])
#   def create_order(self, debug=False):
#     request = OrdersCreateRequest()
#     request.prefer('return=representation')
#     #3. Call PayPal to set up a transaction
#     request.request_body(self.build_request_body())
#     response = self.client.execute(request)
#     if debug:
#       print 'Status Code: ', response.status_code
#       print 'Status: ', response.result.status
#       print 'Order ID: ', response.result.id
#       print 'Intent: ', response.result.intent
#       print 'Links:'
#       for link in response.result.links:
#         print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
#       print 'Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
#                          response.result.purchase_units[0].amount.value)

#     return response

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == "__main__":
  CreateOrder().create_order(debug=True)