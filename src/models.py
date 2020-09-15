from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
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
    #is_available = db.Column(db.Integer, primary_key=True)

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