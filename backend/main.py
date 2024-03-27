# This file will contain the main routes or main endpoints
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))

    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    phone = request.json.get("phone")
    address = request.json.get("address")

    if not first_name or not last_name or not email:
        return jsonify(({"message": "First name, last name, and email are required"}), 400)

    # adding a new entry to the database
    # create python class corresponding to that entry
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address)
    try: 
        db.session.add(new_contact) # add to database session
        db.session.commit() # commit the session
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Contact created successfully!"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create all the different models defined in the database

    app.run(debug=True) # run the application in debug mode so we can see our changes

# Create
# What we need
# First name, last name, email, (phone and address are optional)
