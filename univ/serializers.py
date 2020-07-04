from rest_framework import serializers as s

from univ import models as m


class ScheduleSerializer(s.ModelSerializer):
    class Meta:
        model = m.Schedule
        fields = ('description', 'start_date', 'end_date')


class MajorSerializer(s.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = m.Major
        fields = ('name', 'like', 'schedules')


class JHSerializer(s.ModelSerializer):
    majors = MajorSerializer(many=True)

    class Meta:
        model = m.JH
        fields = ('name', 'like', 'majors')


class SJSerializer(s.ModelSerializer):
    jhs = JHSerializer(many=True)

    class Meta:
        model = m.SJ
        fields = ('sj', 'jhs')


class UnivSerializer(s.ModelSerializer):
    sjs = SJSerializer(many=True)

    class Meta:
        model = m.Univ
        fields = ('name', 'logo', 'review_url', 'like', 'sjs')

