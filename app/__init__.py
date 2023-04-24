# Import necessary modules
import os
import sys
from flask import Flask

# Adds current directory to system path.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configuration requirements
from config import Config
from helpers.worker import make_celery
from dotenv import load_dotenv
load_dotenv()

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
    app.logger.debug('Creating app...')

    # Establish Database Connection
    init_db(app)

    # Create Celery instance 
    worker = make_celery(app)

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