import json
import asyncio
from tasks import handle_notification_task
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

async def observer():
    # Observe for changes / Next notification recipent
    cache = redis_client.get('users_to_notify')
    users_list = json.loads(cache)


    if not users_list: 
        return False
    
    for user in users_list: 
        
        # Conver to proper format for comparison
        next_notification_time_str = user['next_notification_time']
        next_notification_time = datetime.strptime(next_notification_time_str, '%Y-%m-%d %H:%M:%S')

        # Now compare next_notification_time with current time
        current_time = datetime.now()

        if current_time >= next_notification_time:
            await handle_notification_task(user, current_time)


# Create an event loop
loop = asyncio.get_event_loop()

# Create an instance of the scheduler
scheduler = AsyncIOScheduler(event_loop=loop)

# Schedule the task to run every one minute
scheduler.add_job(observer, 'interval', minutes=0.2)

# Start the scheduler
scheduler.start()

# Run the event loop
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
