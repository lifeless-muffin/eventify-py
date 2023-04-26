from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from app.database.users import update_user_preferences, update_user_notification_time
from utilities.notification import generate_user_notification
from database.users import get_user

# Define Blueprint for User route
worker_bp = Blueprint('worker_bp', __name__, url_prefix='/worker')

@worker_bp.route('/users', methods=['POST'])
def worker_updates():
    # current_user_id = get_jwt_identity()
    # current_user = get_current_user()

    # if (current_user['role'] != 'admin'):
    #     return {'status': 'failed', 'message': 'You are not admin'}, 401
    
    data = request.get_json()
    if not data['user_id']:
        return {'status': 'failed', 'message': 'Invalid request'}, 400
    
    update_user_notification_time(data['user_id'], data['time_of_notification'])
    return {'status': 'Successful', 'message': 'User updated'}, 200


@worker_bp.route('/notification/<user_id>', methods=['GET'])

def get_info_for_notification(user_id):

    # Check and validate the user_id
    if not user_id or not get_user(user_id):
        return {'status': 'Failed', 'message': 'Bad Request'}, 400
    
    generate_user_notification(user_id)
    
    return "something at least"
    

    