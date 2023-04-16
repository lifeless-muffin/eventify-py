from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask_pymongo import PyMongo
from flask import current_app

mongo = PyMongo()

def db_init_app(app):
    mongo.init_app(app)
    try:
        client = MongoClient(app.config['MONGO_URI'])
        print('Connected to MongoDB!')
    except ConnectionFailure as e:
        print('Could not connect to MongoDB:', e)

def add_user_if_not_present(user_info):
    # Defining the user collection
    users_collection = mongo.db[current_app.config['MONGO_USERS_COLLECTION']]

    # Check if user already exists in database
    user = users_collection.find_one({'google_id': user_info['sub']})

    if user is None:
        # Add user to database if not already present
        user = {
            'google_id': user_info['sub'],
            'name': user_info['name'],
            'picture': user_info['picture'],
            'email': user_info['email']
        }
        users_collection.insert_one(user)

    return user