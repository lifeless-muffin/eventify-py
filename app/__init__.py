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
from routes.worker import worker_bp

def create_app():
    app = Flask(__name__)
    
    # App configurations
    app.config.from_object(Config)

    # Redis client initalization / Cache
    redis_client = Redis(host='localhost', port=6379, db=0)    
    app.config['REDIS_CLIENT'] = redis_client

    # Establish Database Connection
    init_db(app)

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
    app.register_blueprint(worker_bp)

    return app