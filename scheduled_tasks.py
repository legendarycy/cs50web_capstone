import os
import django
from django.utils import timezone
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Golden_Village.settings')
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from ticket_purchase.models import *

def clear_reservations():
    obj = Tickets.objects.filter(
        timestamp__lt = timezone.now() - timedelta(seconds = 30), 
        status = 'reserved'
    )
    print(f'as of {timezone.now()}:')
    if len(obj) > 0:
        print('the following reservations have been deleted:')
        for each in obj:
            print(f"created: {each.timestamp} | {each.holder.username} | expired by: {(timezone.now() - each.timestamp).total_seconds()} seconds")
        print('\n')
        obj.delete()
    else:
        print('no expired reservations found\n')

# Create an instance of the scheduler
scheduler = BackgroundScheduler()

# Schedule the print_hello function to run every 10 seconds
scheduler.add_job(clear_reservations, 'interval', seconds=10)

# Start the scheduler
scheduler.start()

# Keep the script running
while True:
    user_input = input('Enter "stop" to terminate\n')
    if user_input.lower() == 'stop':
        scheduler.shutdown()
        break