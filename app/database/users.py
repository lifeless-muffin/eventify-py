from app.models.user import Preferences, Users, Notification
from utilities.redis import redis_users_list_cache
from datetime import datetime

def generate_notification_time():

    # Time of notification taken from the user
    current_date = datetime.now().date() # Returns year:month:day
    current_date = current_date.strftime('%Y-%m-%d')
    notification_time_str = '10:40:00' # Hour, Minute, Seconds / Timezone is IST
    notification_time = current_date + " " + notification_time_str

    return notification_time


def add_user_if_not_present(user_info):
    # Check if user already exists in database
    user = get_user(user_info['id'])

    if user is None:

        # Create a new user object with the required fields including preferences 
        notification_time = generate_notification_time()
        notification = Notification(type='email', frequency='all', time_of_notification=notification_time)
        preferences = Preferences(categories=[], notification=notification, language='en', region='us')

        # Create a new User object and populate its fields with the data from user_info
        new_user = Users(
            role='user',
            id=user_info['id'],
            name=user_info['name'],
            email=user_info['email'],
            picture=user_info['picture'],
            preferences=preferences
        )

        # Save the new user to the database
        user = new_user
        new_user.save()

    # Return user / either existing or new user
    redis_users_list_cache()
    return user


def get_user(user_id):
    user = Users.objects(id=user_id).first()
    if user:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'preferences': user.preferences,    
            'email': user.email,
            'picture': user.picture
        }
        return user_dict
    return None


def update_user_preferences(user_id, preferences_object):

    user = Users.objects.get(id=user_id)

    # Create a new user object with the required fields including preferences 
    noti_short = preferences_object['notification']
    
    notification = Notification(type=noti_short['type'], frequency=noti_short['frequency'], time_of_notification=noti_short['time_of_notification'])
    preferences = Preferences(categories=preferences_object['categories'], notification=notification, language=preferences_object['language'], region=preferences_object['region'])

    setattr(user, 'preferences', preferences)
    user.save()

    # here we will request for cache update
    redis_users_list_cache()
    return user


def update_user_notification_time(user_id, updated_user_notification_time):

    user = Users.objects.get(id=user_id)
    pref_initial = user['preferences']
    noti_initial = user['preferences']['notification']

    if not updated_user_notification_time:
        # Check if it's correct or whehter it even exists
        return None

    # update the user_notification time / next_notification_time from preferences.notification
    notification = Notification(type=noti_initial['type'], frequency=noti_initial['frequency'], time_of_notification=updated_user_notification_time)
    preferences = Preferences(categories=pref_initial['categories'], notification=notification, language=pref_initial['language'], region=pref_initial['region'])

    setattr(user, 'preferences', preferences)
    user.save()

    # here we will request for cache update
    redis_users_list_cache()
    return user


