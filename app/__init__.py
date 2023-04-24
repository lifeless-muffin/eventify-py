# Import necessary modules
import os
import sys
import json
from redis import Redis
from flask import Flask

# Configuration requirements
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from config import Config

# Database / Authentication configuration imports
from database.database import init_db
from auth.auth import init_auth, load_user, login_manager
from flask_jwt_extended import JWTManager

# Routes and blueprints
from routes import main_bp
from routes.user import user_bp

def create_app():
    app = Flask(__name__)
    
    # App configurations
    app.config.from_object(Config)
    
    # Establish Database Connection
    init_db(app)

    # Redis client initalization / Cache
    redis_client = Redis(host='localhost', port=6379, db=0)

    redis_client.set('users_to_notify', json.dumps([{'next_notification_time': '2023-04-23 23:30:00', 'user_id': '01'}]))

    # Initalize JWT Manager for token authentication
    jwt = JWTManager(app)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.user_loader(load_user)
    app.logger.info('Login manager initialized')

    # Authentication initialization
    init_auth(app)
    
    # Importing Blueprints /
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app