from flask import Blueprint, redirect, url_for, session, current_app
from authlib.integrations.flask_client import OAuth
from app.database import add_user_if_not_present

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

oauth = OAuth()

@auth_bp.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth_bp.authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorized')
def authorized():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    add_user_if_not_present(user_info)

    session['profile'] = user_info
    return redirect('/')

def init_app(app):
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