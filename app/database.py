from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import current_app
from pymongo.mongo_client import MongoClient
from config import Config

# Create a new client and connect to the server
client = MongoClient(Config.MONGO_URI)

# Send a ping to confirm a successful connection
def establish_connection(app):
    global client
    try:
        client.admin.command('ping')
        app.config['DB_CLIENT'] = client
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


def add_user_if_not_present(user_info):
    users_collection = client[current_app.config['MONGO_DBNAME']]['users']

    # Check if user already exists in database
    user = users_collection.find_one({'google_id': user_info['id']})

    if user is None:
        # Add user to database if not already present
        user = {
            'google_id': user_info['id'],
            'name': user_info['name'],
            'picture': user_info['picture'],
            'email': user_info['email']
        }
        users_collection.insert_one(user)

    return user


def get_user_info_from_db(user_id):
    users_collection = client[current_app.config['MONGO_DBNAME']]['users']
    found_user = users_collection.find_one({'google_id': user_id})
    return found_user
