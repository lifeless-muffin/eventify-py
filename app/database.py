from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from flask import current_app
from pymongo.mongo_client import MongoClient
from config import Config

# Create a new client and connect to the server
client = MongoClient(Config.MONGO_URI)

def get_users_collection():
    return client[current_app.config['MONGO_DBNAME']]['users']

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
    users_collection = get_users_collection()

    # Check if user already exists in database
    user = users_collection.find_one({'id': user_info['id']})

    if user is None:
        # Add user to database if not already present
        user = {
            'id': user_info['id'],
            'name': user_info['name'],
            'picture': user_info['picture'],
            'email': user_info['email']
        }

        users_collection.insert_one(user)

    return user


def get_user_info_from_db(user_id):
    users_collection = get_users_collection()
    found_user = users_collection.find_one({'id': user_id})
    return found_user

def update_user(user_id, new_user_data):
    # Fetch users's old information from database
    users_collection = get_users_collection()
    old_user_data = users_collection.find_one({'id': user_id})

    # Iterate through the keys of the new user data
    for key in new_user_data:
        # If the value of a key is different in the new data, update it in the database
        if key not in old_user_data.keys() or new_user_data[key] != old_user_data[key]:
            users_collection.update_one(
                {"id": user_id},
                {"$set": {key: new_user_data[key]}}
            )
