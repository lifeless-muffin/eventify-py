from app.models.user_model import Preferences, Users, Notification
from database.database import db

def add_user_if_not_present(user_info):
    # Check if user already exists in database
    user = get_user(user_info['id'])

    if user is None:

        # Create a new user object with the required fields including preferences 
        notification = Notification(type='email', frequency='all', time_of_notification='4:00')
        preferences = Preferences(categories=[], notification=notification, language='en', region='us')

        # Create a new User object and populate its fields with the data from user_info
        new_user = Users(
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

def update_user(user_id, updates):
    user = Users.objects.get(id=user_id)
    for key, value in updates.items():
        setattr(user, key, value)
    user.save()
    return user