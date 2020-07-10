import os
import csv

import django
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from univ.models import Univ, SJ, JH, Major, Schedule


with open('csv/university.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if not Univ.objects.filter(name=row[0]):
            Univ.objects.create(name=row[0], logo=row[1], review_url=row[2])

for univ in Univ.objects.all():
    univ = Univ.objects.get(name=univ)
    SJ.objects.create(univ=univ, sj='수시')
    SJ.objects.create(univ=univ, sj='정시')

    jh_file = f'csv/{univ.name}/jh.csv'
    major_file = f'csv/{univ.name}/major.csv'
    schedule_file = f'csv/{univ.name}/schedule.csv'

    if os.path.isfile(jh_file):
        with open(jh_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                univ = row[0]
                sj = row[1]
                jh = row[2]
                if not JH.objects.filter(Q(sj__univ__name=univ) & Q(sj__sj=sj) & Q(name=jh)):
                    JH.objects.create(sj=SJ.objects.get(Q(univ__name=univ) & Q(sj=sj)), name=jh)

    if os.path.isfile(major_file):
        with open(major_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                univ = row[0]
                sj = row[1]
                jh = row[2]
                major = row[3]
                if not Major.objects.filter(Q(jh__sj__univ__name=univ) & Q(jh__sj__sj=sj) & Q(jh__name=jh) & Q(name=major)):
                    Major.objects.create(jh=JH.objects.get(Q(sj__univ__name=univ) & Q(sj__sj=sj) & Q(name=jh)), name=major)

    if os.path.isfile(schedule_file):
        with open(schedule_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                univ = row[0]
                sj = row[1]
                jh = row[2]
                major = row[3]
                description = row[4]
                start_date = make_aware(parse_datetime(row[5]))
                end_date = make_aware(parse_datetime(row[6]))
                if not Schedule.objects.filter(
                        Q(major__jh__sj__univ__name=univ) &
                        Q(major__jh__sj__sj=sj) &
                        Q(major__jh__name=jh) &
                        Q(major__name=major) &
                        Q(description=description)
                        ):
                    Schedule.objects.create(
                            major=Major.objects.get(
                                Q(jh__sj__univ__name=univ) &
                                Q(jh__sj__sj=sj) &
                                Q(jh__name=jh) &
                                Q(name=major)
                                ),
                            description=description,
                            start_date=start_date,
                            end_date=end_date,
                            )
                else:
                    schedule = Schedule.objects.get(
                        Q(major__jh__sj__univ__name=univ) &
                        Q(major__jh__sj__sj=sj) &
                        Q(major__jh__name=jh) &
                        Q(major__name=major) &
                        Q(description=description)
                        )
                    schedule.start_date = start_date
                    schedule.end_date = end_date
                    schedule.save()
