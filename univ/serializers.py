from rest_framework import serializers as s
from django.utils.timezone import make_aware
from pytz import timezone

from univ import models as m
import datetime


class ScheduleSerializer(s.ModelSerializer):
    is_valid = s.SerializerMethodField()
    start_date = s.SerializerMethodField()
    end_date = s.SerializerMethodField()

    def get_is_valid(self, obj):
        if make_aware(datetime.datetime.now()) < obj.end_date:
            return 1
        else:
            return 0

    def get_start_date(self, obj):
        return obj.start_date.astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-%M-%S')

    def get_end_date(self, obj):
        return obj.end_date.astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-%M-%S')

    class Meta:
        model = m.Schedule
        fields = ('is_valid', 'description', 'start_date', 'end_date')


class MajorSerializer(s.ModelSerializer):
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = m.Major
        fields = ('name', 'schedules')


class MajorListSerializer(s.ModelSerializer):
    class Meta:
        model = m.Major
        fields = ('name',)


class JHSerializer(s.ModelSerializer):
    majors = s.SerializerMethodField()

    def get_majors(self, obj):
        if not self.context.get('majors'):
            return MajorSerializer(obj.majors, many=True, context=self.context).data
        all_majors = self.context.get('majors')
        majors_in_this_jh = [major for major in all_majors if major.jh == obj]
        return MajorSerializer(majors_in_this_jh, many=True, context=self.context).data

    class Meta:
        model = m.JH
        fields = ('name', 'majors')


class JHListSerializer(s.ModelSerializer):
    majors = s.SerializerMethodField()

    def get_majors(self, obj):
        if not self.context.get('majors'):
            return MajorListSerializer(obj.majors, many=True, context=self.context).data
        all_majors = self.context.get('majors')
        majors_in_this_jh = [major for major in all_majors if major_jh == obj]
        return MajorListSerializer(majors_in_this_jh, many=True, context=self.context).data

    class Meta:
        model = m.JH
        fields = ('name', 'majors')


class SJSerializer(s.ModelSerializer):
    jhs = s.SerializerMethodField()

    def get_jhs(self, obj):
        if not self.context.get('jhs'):
            return JHSerializer(obj.jhs, many=True, context=self.context).data
        all_jhs = self.context.get('jhs')
        jhs_in_this_sj = [jh for jh in all_jhs if jh.sj == obj]
        return JHSerializer(jhs_in_this_sj, many=True, context=self.context).data

    class Meta:
        model = m.SJ
        fields = ('sj', 'jhs')


class SJListSerializer(s.ModelSerializer):
    jhs = s.SerializerMethodField()

    def get_jhs(self, obj):
        if not self.context.get('jhs'):
            return JHListSerializer(obj.jhs, many=True, context=self.context).data
        all_jhs = self.context.get('jhs')
        jhs_in_this_sj = [jh for jh in all_jhs if jh.sj == obj]
        return JHListSerializer(jhs_in_this_sj, many=True, context=self.context).data

    class Meta:
        model = m.SJ
        fields = ('sj', 'jhs')


class UnivSerializer(s.ModelSerializer):
    sjs = s.SerializerMethodField()

    def get_sjs(self, obj):
        if not self.context.get('sjs'):
            return SJSerializer(obj.sjs, many=True, context=self.context).data
        all_sjs = self.context.get('sjs')
        sjs_in_this_univ = [sj for sj in all_sjs if sj.univ == obj]
        return SJSerializer(sjs_in_this_univ, many=True, context=self.context).data

    class Meta:
        model = m.Univ
        fields = ('name', 'logo', 'review_url', 'sjs')


class UnivListSerializer(s.ModelSerializer):
    sjs = s.SerializerMethodField()

    def get_sjs(self, obj):
        if not self.context.get('sjs'):
            return SJListSerializer(obj.sjs, many=True, context=self.context).data
        all_sjs = self.context.get('sjs')
        sjs_in_this_univ = [sj for sj in all_sjs if sj.univ == obj]
        return SJListSerializer(sjs_in_this_univ, many=True, context=self.context).data

    class Meta:
        model = m.Univ
        fields = ('name', 'logo', 'review_url', 'sjs')
