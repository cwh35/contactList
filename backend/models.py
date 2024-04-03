# This file will contain all of our database models
from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # this means this is the key we use for indexing and it must be unique for every single entry in the database
    first_name = db.Column(db.String(50), unique=False, nullable=False) # cannot pass a null value
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.BigInteger, unique=True, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)

    def to_json(self):
        # takes the different fields on our object and converts them into a dictionary
        # we can then convert this dictionary to JSON, which we can pass from our API
        return {
            "id": self.id,
            "firstName": self.first_name, # use camel case for JSON keys, snake case for python variables
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }