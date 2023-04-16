import os
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from flask import Flask
import secrets
from config import Config
from database import db_init_app
from auth.auth import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    db_init_app(app)
    init_app(app)
    
    # Importing Blueprints /

    return app