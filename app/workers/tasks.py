import time
import asyncio
from datetime import datetime, timedelta

def calculate_next_notification_time(user, current_time):

    # Retrieve essentails 
    frequency = user['frequency']
    last_notification_time = user['last_notification_time']

    # Convert last notification time to datetime object
    last_notification_time = datetime.strptime(last_notification_time, '%Y-%m-%d %H:%M:%S')
    
    # Calculate next notification time based on frequency
    if frequency == 'daily':
        next_notification_time = last_notification_time + timedelta(days=1)
    elif frequency == 'weekly':
        next_notification_time = last_notification_time + timedelta(weeks=1)
    elif frequency == 'every other day':
        # Assume frequency is in hours
        next_notification_time = last_notification_time + timedelta(days=2)
    else:
        next_notification_time = last_notification_time + timedelta(days=1)
    
    # If next notification time is in the past, add the frequency until it's in the future
    while next_notification_time < current_time:
        next_notification_time += timedelta(hours=int(frequency))
    
    return next_notification_time.strftime('%Y-%m-%d %H:%M:%S')


async def update_user_in_db(user, current_time):
    # request to backend to update the user
    next_notification_time = calculate_next_notification_time(user, current_time)
    notify_result = notify_user(user, next_notification_time)

    pass

async def notify_user(user):
    # handle notification and stuff
    pass

async def handle_notification_task(user, current_time):

    pass