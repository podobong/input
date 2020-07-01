from rest_framework.views import APIView
from rest_framework.response import Response

from univ.models import Schedule, University
from univ.serializers import ScheduleSerializer, ReviewSerializer


class ScheduleList(APIView):
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class ReviewList(APIView):
    def get(self, request):
        universities = University.objects.all()
        serializer = ReviewSerializer(universities, many=True)
        return Response(serializer.data)

