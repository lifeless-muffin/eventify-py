from celery import Celery
from datetime import datetime, timedelta
from celery.schedules import crontab
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def get_user_list():
    """
    Get the user list from the cache.
    """
    user_list = []
    user_dict_list = redis_client.lrange('users_list', 0, -1)
    for user_dict in user_dict_list:
        user_list.append(eval(user_dict))
    return user_list

def set_user_list(user_list):
    """
    Set the user list to the cache.
    """
    user_dict_list = []
    for user in user_list:
        user_dict = str(user)
        user_dict_list.append(user_dict)
    redis_client.delete('users_list')
    redis_client.rpush('users_list', *user_dict_list)

def is_notification_time(next_notification_time):
    """
    Check if the next_notification_time is less than or equal to the current time.
    """
    current_time = datetime.now()
    return next_notification_time <= current_time

def send_notification(user_id):
    """
    Send a notification to the user with the given user_id.
    """
    # TODO: Implement notification method here.
    pass

def process_user_list():
    """
    Process the user list to determine if any users need to be notified.
    """
    user_list = get_user_list()
    for user in user_list:
        if is_notification_time(user['next_notification_time']):
            send_notification(user['id'])
            # Update the next_notification_time for the user.
            user['next_notification_time'] = datetime.now() + timedelta(days=1)
    # Update the user list in the cache.
    set_user_list(user_list)

# Create the Celery instance.
celery = Celery()

# Configure Celery.
celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/0'
celery.conf.beat_schedule = {
    'process_user_list_task': {
        'task': 'process_user_list',
        'schedule': crontab(minute='*/1'),
    },
}

# Create the task to process the user list.
@celery.task(name='process_user_list')
def process_user_list_task():
    process_user_list()
