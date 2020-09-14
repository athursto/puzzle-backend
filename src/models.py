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
<<<<<<< HEAD
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)
=======
    order_id = db.relationship('Order') #adding in order relationship
>>>>>>> 3a766b7cb1ad79b810dd46ac46770610247fd0ce

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            # do not serialize the password, its a security breach
            "order_id": list(map(lambda x: x.serialize(), self.order_id))
        }



class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_puzzle = db.Column(db.String(50), unique=True, nullable=False)
    picture_of_puzzle = db.Column(db.LargeBinary)
    picture_of_box = db.Column(db.LargeBinary) 
    number_of_pieces = db.Column(db.Integer, unique=False, nullable=False) 
    age_range = db.Column(db.String(10), unique=False, nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, unique=False, nullable=False)
    borrower = db.Column(db.Integer, primary_key=True)
    is_available = db.Column(db.Boolean(), unique=False, nullable=False)
    order_id = db.relationship('Order') #adding in order relationship


    # def __repr__(self):
    #     return '<Puzzle / %r>' % self.name_of_puzzle

    def serialize(self):
        return {
        "id": self.id,
        "name_of_puzzle": self.name_of_puzzle,
        "order_id": list(map(lambda x: x.serialize(), self.order_id))
         # do not serialize the password, its a security breach
                }

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, unique=False, nullable=False)
    weight = db.Column(db.Float, unique=False, nullable=False)
    payment_id = db.Column(db.String, unique=True, nullable=False)
    puzzle_id = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    puzzle_id = db.Column(db.Integer, db.ForeignKey("Puzzle.id"))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            #"email": self.email,
            # do not serialize the password, its a security breach
            "address": self.address,
            "order_id": self.order_id
        }