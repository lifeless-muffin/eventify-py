from flask import Blueprint, current_app
from flask_login import login_required, current_user

main_bp = Blueprint('main_bp', __name__, url_prefix='/')

@main_bp.route('/')
def home():
    return 'Hey!! you reached the home innit?'

@main_bp.route('/home')
@login_required
def protected_home():
    return 'Welcome'
