from rest_framework import serializers as s

from univ import models as m


class ScheduleSerializer(s.ModelSerializer):
    class Meta:
        model = m.Schedule
        fields = ('description', 'start_date', 'end_date')


class MajorSerializer(s.ModelSerializer):
    schedules = ScheduleSerializer(many=True)
    like = s.SerializerMethodField()

    def get_like(self, obj):
        unique_id = self.context.get('request').GET.get('id')
        if not unique_id:
            return 0
        device = m.Device.objects.get(unique_id=unique_id)
        if obj in device.majors.all():
            return 1
        return 0

    class Meta:
        model = m.Major
        fields = ('name', 'like', 'schedules')


class JHSerializer(s.ModelSerializer):
    majors = MajorSerializer(many=True)
    like = s.SerializerMethodField()

    def get_like(self, obj):
        unique_id = self.context.get('request').GET.get('id')
        if not unique_id:
            return 0
        device = m.Device.objects.get(unique_id=unique_id)
        for major in obj.majors.all():
            if major in device.majors.all():
                return 1
        return 0

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
    like = s.SerializerMethodField()

    def get_like(self, obj):
        unique_id = self.context.get('request').data.get('id')
        if not unique_id:
            return 0
        try:
            device = m.Device.objects.get(unique_id=unique_id)
        except m.Device.DoesNotExist:
            raise m.Device.DoesNotExist
        for sj in obj.sjs.all():
            for jh in sj.jhs.all():
                for major in jh.majors.all():
                    if major in device.majors.all():
                        return 1
        return 0

    class Meta:
        model = m.Univ
        fields = ('name', 'logo', 'review_url', 'like', 'sjs')
