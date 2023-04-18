import os

class Config:
    # Google cloud configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Atlast MongoDB configuration
    MONGO_DBNAME = 'eventify_db'
    MONGO_USERS_COLLECTION = 'users'
    MONGO_URI = os.environ.get('MONGO_URI')

    # Jwt / Flask security configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')