from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask_pymongo import PyMongo
from flask import current_app

mongo = PyMongo()

def db_init_app(app):
    mongo.init_app(app)
    try:
        client = MongoClient(app.config['MONGO_URI'])
        mongo.cx = client[app.config['MONGO_DBNAME']]
        print('Connected to MongoDB!')
    except ConnectionFailure as e:
        print('Could not connect to MongoDB:', e)

def add_user_if_not_present(user_info):
    # Defining the user collection
    print(mongo.cx['users'], "this is mongodb")
    users_collection = mongo.cx['users']

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