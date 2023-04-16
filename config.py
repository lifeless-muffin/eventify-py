import os

class Config:
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    MONGO_DBNAME = 'eventify_db'
    MONGO_USERS_COLLECTION = 'users'
    MONGO_URI = os.environ.get('MONGO_URI')