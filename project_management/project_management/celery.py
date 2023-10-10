# celery.py

from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_management.settings')

app = Celery('project_management')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.dashboard(bind=True)
def send_reminder_email(self, user_email, subject, message):
    from django.core.mail import send_mail
    send_mail(subject, message, 'greeshma150295@gmail.com', [user_email])

# # Define the Celery beat schedule to run the task daily at a specific time.
# app.conf.beat_schedule = {
#     'send-reminders-daily': {
#         'task': 'project_management.tasks.send_reminders',
#         'schedule': crontab(hour=0, minute=5),  # Adjust the time as needed
#     },
# }