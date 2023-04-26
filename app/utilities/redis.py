import json
from flask import current_app
from models.user import Users, Preferences, Notification

# We could do the thing -- here

def redis_users_list_cache():

    redis_client = current_app.config['REDIS_CLIENT'] 
    users_list = Users.objects()
    redis_users_list = []
    
    for user in users_list:

        user_id = user.id

        if user.preferences is not None and user.preferences.notification is not None:
            frequency = user.preferences.notification.frequency
            time_of_notification = user.preferences.notification.time_of_notification
        else:
            print(f"User {user.name} has no notification preferences")

        if not user:
            # handle that
            print('Not user')
            return None

        redis_users_list.append({
            'user_id': user_id, 
            'time_of_notification': time_of_notification,
            'frequency': frequency
        })
            

    redis_client.set('cached-users-list', json.dumps(redis_users_list))
