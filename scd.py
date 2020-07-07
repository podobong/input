import os
import time
from datetime import datetime, timedelta

from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from univ.models import Schedule
from temp import send_fcm_notification


KST = timezone('Asia/Seoul')


def notify():
    schedules = Schedule.objects.all()
    for schedule in schedules:
        liked_users = schedule.major.devices.all()
        tokens = [user.token for user in liked_users]
        start_date = schedule.start_date
        day_before = timedelta(days=1)
        now_hour = KST.localize(datetime.now().replace(minute=0, second=0, microsecond=0))
        if now_hour == (start_date - day_before):
            print(tokens[0])
            print(schedule.description)
            send_fcm_notification(tokens[0], '제목', schedule.description)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=KST)
    scheduler.start()
    scheduler.add_job(notify, 'interval', seconds=5)

    while True:
        time.sleep(1)
