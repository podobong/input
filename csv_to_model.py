import os
import csv

import django
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_awake

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from univ.models import University, MajorBlock, Jeonhyeong, Schedule


with open('csv/university.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if not University.objects.filter(name=row[0]):
            University(name=row[0], logo=row[1], review_url=row[2]).save()

for univ in University.objects.all():
    jeonhyeong_file = f'csv/{univ.name}/jeonhyeong.csv'
    major_block_file = f'csv/{univ.name}/major_block.csv'
    schedule_file = f'csv/{univ.name}/schedule.csv'

    if os.path.isfile(jeonhyeong_file):
        with open(jeonhyeong_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if not Jeonhyeong.objects.filter(Q(university__name=row[0]) & Q(susi_jeongsi=row[1])
                        & Q(year=row[2]) & Q(name=row[3])):
                    univ = University.objects.get(name=row[0])
                    Jeonhyeong(university=univ, susi_jeongsi=row[1], year=row[2], name=row[3]).save()

    if os.path.isfile(major_block_file):
        with open(major_block_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if not MajorBlock.objects.filter(Q(university__name=row[0])
                        & Q(susi_jeongsi=row[1]) & Q(name=row[2])):
                    univ = University.objects.get(name=row[0])
                    MajorBlock(university=univ, susi_jeongsi=row[1], name=row[2]).save()
    
    if os.path.isfile(schedule_file):
        with open(schedule_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                jeonhyeong_info = row[0].split('|')
                jeonhyeong = Jeonhyeong.objects.get(
                        Q(university__name=jeonhyeong_info[0])
                        & Q(susi_jeongsi=jeonhyeong_info[1])
                        & Q(year=jeonhyeong_info[2])
                        & Q(name=jeonhyeong_info[3])
                )
                major_block_info = row[1].split('|')
                major_block = MajorBlock.objects.get(
                        Q(university__name=major_block_info[0])
                        & Q(susi_jeongsi=major_block_info[1])
                        & Q(name=major_block_info[2])
                )
                start_date = make_aware(parse_datetime(row[3]))
                end_date = make_aware(parse_datetime(row[4]))
                if not Schedule.objects.filter(jeonhyeong=jeonhyeong).filter(major_block=major_block).filter(description=row[2]):
                    Schedule(jeonhyeong=jeonhyeong, major_block=major_block, description=row[2], start_date=start_date, end_date=end_date).save()
                else:
                    schedule = Schedule.objects.filter(jeonhyeong=jeonhyeong).filter(major_block=major_block).get(description=row[2])
                    schedule.start_date = start_date
                    schedule.end_date = end_date
                    schedule.save()

