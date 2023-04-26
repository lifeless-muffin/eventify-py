from flask import Blueprint, redirect, url_for, session, current_app
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_jwt_extended import jwt_required, create_access_token

# Custom modules
from database.users import add_user_if_not_present, get_user

# Define Blueprint for authentication
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

# Create the OAuth instance
oauth = OAuth()

# Creat the LoginManager instance
login_manager = LoginManager()

# Define the User class
class User(UserMixin):
    def __init__(self, user_info):

        self.id = user_info.get('id')
        self.name = user_info.get('name')
        self.email = user_info.get('email')
        self.picture = user_info.get('picture')

    def get_id(self):
        return str(self.id)

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    current_app.logger.info('Loading user: %s', user_id)

    # Load the user from the database
    user_info = get_user(user_id)

    if user_info:
        user = User(user_info)
        current_app.logger.info('User found: %s', user_id)
        return user
    else:
        current_app.logger.warning('User not found: %s', user_id)
        return None


@auth_bp.route('/google/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth_bp.authorized', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/login')
@jwt_required
def login_with_token():
    return {'status': 'success', 'data': {'user_id': current_user.get_id()}}, 200


@auth_bp.route('/google/authorized')
def authorized():
    google = oauth.create_client('google')
    google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    stored_user = add_user_if_not_present(user_info)
    print('User Reigstered: ', stored_user)

    get_user_as_dict = get_user(stored_user.id)

    # Create the User object and login the user
    user = User(get_user_as_dict)
    login_user(user)

    # Generate a JWT token and return it to the client
    access_token = create_access_token(identity=user.get_id())
    return {'access_token': access_token}, 200


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return {'status': 'success'}, 200

def init_auth(app):
    oauth.init_app(app)

    with app.app_context():
        google = oauth.register(
            name='google',
            client_id=current_app.config['GOOGLE_CLIENT_ID'],
            client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_params=None,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            api_base_url='https://www.googleapis.com/oauth2/v1/',
            userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
            client_kwargs={'scope': 'openid email profile'},
        )

    app.register_blueprint(auth_bp)