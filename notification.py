# -*- coding: utf-8 -*-
import os
import time
import requests
import json
from datetime import datetime, timedelta

from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.keys import firebase
from univ.models import Schedule

KST = timezone('Asia/Seoul')


def send_fcm_notification(ids, title, body):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Authorization': firebase.key,
        'Content-Type': 'application/json; UTF-8',
    }
    content = {
        'to': ids,
        'notification': {'title': title, 'body': body},
        "data": {"id": "id"}
    }
    requests.post(url, data=json.dumps(content), headers=headers)


def notify():
    schedules = Schedule.objects.all()
    for schedule in schedules:
        liked_users = schedule.major.devices.all()
        tokens = [user.token for user in liked_users]
        day_before = timedelta(days=1)
        now_hour = KST.localize(datetime.now().replace(minute=0, second=0, microsecond=0))
        if now_hour == (schedule.end_date - day_before):
            for token in tokens:
                send_fcm_notification(token, f'{schedule.description} 마감 하루 전이에요!', schedule.description)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=KST)
    scheduler.start()
    scheduler.add_job(notify, 'interval', hours=1)

    while True:
        time.sleep(1)
