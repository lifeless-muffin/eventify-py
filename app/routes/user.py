from flask import Blueprint, redirect, url_for, request, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import update_user

# Define Blueprint for User route
user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

# Define route for updating user preferences / validate the token
@user_bp.route('/update', methods=['POST'])
@jwt_required()
def update_user_preferences():
    
    # get user identity / preferences from request
    user_id = get_jwt_identity()
    data = request.get_json()
    updated_preferences = data['preferences'] 

    # Find and update user preferences in the DB
    if (updated_preferences):
        # Update user preferences
        res = update_user(user_id, {'preferences': updated_preferences})
        updated_user_object = res

    else:
        return {'status': 'failed', 'message': 'Empty user preferences'}, 400

    return {'status': 'success', 'message': 'User preferences updated'}, 200