# This will contain the main configuration for the application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

# CORS = Cross Origin Requests
# This lets us send requests to the backend from a different URL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # disables tracking all modifications made to the database

# create instance of database
# gives access to the database created above
# allows us to use CRUD functions: create, read, update, and delete
db = SQLAlchemy(app)
