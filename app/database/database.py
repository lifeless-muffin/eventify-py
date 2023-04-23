from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from config import Config

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