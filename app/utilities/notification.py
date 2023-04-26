from datetime import datetime
from utilities.tmdb import get_content
from database.users import get_user

def generate_notification_time():

    # Time of notification taken from the user
    current_date = datetime.now().date() # Returns year:month:day
    current_date = current_date.strftime('%Y-%m-%d')
    notification_time_str = '10:40:00' # Hour, Minute, Seconds / Timezone is IST
    notification_time = current_date + " " + notification_time_str

    return notification_time


def generate_user_notification(user_id):
    # Generate user notification based on preferences

    user_info = get_user(user_id)
    get_content(user_info)

    return "This is the notification stuff yknow"

    