from rest_framework import serializers as s

from django.utils.timezone import make_aware
from univ import models as m
import datetime

class ScheduleSerializer(s.ModelSerializer):
    is_valid = s.SerializerMethodField()
    start_date = s.SerializerMethodField()
    end_date = s.SerializerMethodField()

    def get_is_valid(self, obj):
        if make_aware(datetime.datetime.now()) < obj.start_date:
            return 1
        else:
            return 0

    def get_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d-%H-%M-%S')

    def get_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d-%H-%M-%S')

    class Meta:
        model = m.Schedule
        fields = ('is_valid', 'description', 'start_date', 'end_date')


class MajorSerializer(s.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = m.Major
        fields = ('name', 'schedules')


class JHSerializer(s.ModelSerializer):
    majors = s.SerializerMethodField()

    def get_majors(self, obj):
        all_majors = self.context.get('majors')
        majors_in_this_jh = [major for major in all_majors if major.jh == obj]
        return MajorSerializer(majors_in_this_jh, many=True, context=self.context).data

    class Meta:
        model = m.JH
        fields = ('name', 'majors')


class SJSerializer(s.ModelSerializer):
    jhs = s.SerializerMethodField()

    def get_jhs(self, obj):
        all_jhs = self.context.get('jhs')
        jhs_in_this_sj = [jh for jh in all_jhs if jh.sj == obj]
        return JHSerializer(jhs_in_this_sj, many=True, context=self.context).data

    class Meta:
        model = m.SJ
        fields = ('sj', 'jhs')


class UnivSerializer(s.ModelSerializer):
    sjs = s.SerializerMethodField()

    def get_sjs(self, obj):
        all_sjs = self.context.get('sjs')
        sjs_in_this_univ = [sj for sj in all_sjs if sj.univ == obj]
        return SJSerializer(sjs_in_this_univ, many=True, context=self.context).data

    class Meta:
        model = m.Univ
        fields = ('name', 'logo', 'review_url', 'sjs')
