import os
import logging

class Config:
    # Flaks configurations
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = 'logs/app.log'
    FLASK_ENV = 'development'

    # Google cloud configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Atlast MongoDB configuration
    MONGO_DBNAME = 'movkit'
    MONGO_USERS_COLLECTION = 'users'
    MONGO_URI = os.environ.get('MONGO_URI')

    # Jwt / Flask security configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = False

    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://mansoorroeen71:MyygOBZNHQmIewhs@cluster0.d7t5typ.mongodb.net/movkit?retryWrites=true&w=majority',
        'db': 'movkit',
        'username': 'mansoorroeen71 ',
        'password': 'MyygOBZNHQmIewhs',
        'authentication_source': 'admin',
        'tls': True
    }

    # Celery / redis configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
