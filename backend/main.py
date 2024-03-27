# This file will contain the main routes or main endpoints
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))

    return jsonify({"contacts": json_contacts})


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create all the different models defined in the database

    app.run(debug=True) # run the application in debug mode so we can see our changes

# Create
# What we need
# First name, last name, email, (phone and address are optional)
