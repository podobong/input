from rest_framework import serializers

from univ.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'university', 'sj', 'jh', 'block', 'description', 'start_date', 'end_date')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('name', 'review_url')
