from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)
    order_id = db.relationship('Order', backref = 'user') #adding in order relationship
    puzzles_owned = db.relationship('Puzzle', backref='user') #adding in puzzle relationship 


    def __repr__(self):
        return '<User %r>' % self.username

    def validate_password(self, password):
        if self.password != password:
            return False

        return True

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "username": self.username,
           

            # do not serialize the password, its a security breach
            # "order_id": list(map(lambda x: x.serialize(), self.order_id))
        }



class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_puzzle = db.Column(db.String(50), unique=True, nullable=False)
    picture_of_puzzle = db.Column(db.LargeBinary)
    picture_of_box = db.Column(db.LargeBinary) 
    number_of_pieces = db.Column(db.Integer, unique=False, nullable=False) 
    age_range = db.Column(db.String(10), unique=False, nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=False)
    borrower = db.Column(db.Integer, primary_key=True)
    is_available = db.Column(db.Boolean(), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.relationship('Order', backref='puzzle')
    #owner_id = db.Column(db.Integer, unique=False, nullable=False) **delete this
    #is_available = db.Column(db.Integer, primary_key=True)
    #borrower = db.Column(db.Integer, primary_key=True)
    #is_available = db.Column(db.LargeBinary (), unique=False, nullable=False)
    # order_id = db.relationship('Order') #adding in order relationship


    def __repr__(self):
        return '<Puzzle / %r>' % self.name_of_puzzle

    def serialize(self):
        return {
            "id": self.id,
            "name_of_puzzle": self.name_of_puzzle,
            "picture_of_puzzle": self.picture_of_puzzle,
            "picture_of_box": self.picture_of_box,
            "number_of_pieces": self.number_of_pieces,
            "age_range": self.age_range,
            "category": self.category,
            "owner_id": self.owner_id,
            # "is_available": self.is_available

            # do not serialize the password, its a security breach
        }
    def serialize(self):
        return {
        "id": self.id,
        "name_of_puzzle": self.name_of_puzzle,
        "user": {"name": self.User.full_name,
                    "id": self.User.id}
         # do not serialize the password, its a security breach
                }

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), unique=False, nullable=False)
    weight = db.Column(db.Float, unique=False, nullable=False)
    payment_id = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    puzzle_id = db.Column(db.Integer, db.ForeignKey("puzzle.id"))

    def __repr__(self):
        return '<Order %r>' % self.order_info

    def serialize(self):
        return {
             "id": self.id,
             #"email": self.email,
            # do not serialize the password, its a security breach
             "address": self.address,
             "order_id": self.order_id
         }
