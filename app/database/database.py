from flask import Flask
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from config import Config
from models import collections

db = MongoEngine()

def init_db(app):
    db.init_app(app)
    client = get_mongo_client(app)
    app.config['DB_INSTANCE'] = client.get_database()
    print("Connected to MongoDB!")

def get_mongo_client(app):
    with app.app_context():
        mongo_uri = Config.MONGODB_SETTINGS["host"]
        mongo_client = MongoClient(mongo_uri)
        return mongo_client

def get_collection(app, collection_name):
    """
    Returns a reference to the specified collection
    """
    with app.app_context():
        client = get_mongo_client(app)
        db = client.get_database()
        model = collections[collection_name]
        collection = model.objects.using(db).all()
        return collection