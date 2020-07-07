from django.db.models import Q
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from univ.models import Univ, Major, Device
from univ.serializers import UnivSerializer


class UnivList(APIView):
    def get(self, request):
        serializer = UnivSerializer(Univ.objects.all(), many=True, context={'request': request})
        try:
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response(
                    {'error': 'Device does not exist. To add a new device, use POST method.'},
                    status=status.HTTP_400_BAD_REQUEST,
                    )

    def post(self, request):
        # Parameter existence check
        required_parameters = ('id', 'univ0', 'jh0', 'major0')
        for param in required_parameters:
            if not param in request.data:
                return Response(
                        {'error': f'"{param}" parameter is required.'},
                        status=status.HTTP_400_BAD_REQUEST,
                        )
        # Create device info
        values = {param: request.data.get(param) for param in required_parameters}
        try:
            device = Device.objects.create(unique_id=values.get('id'))
        except IntegrityError:
            return Response({'error': 'Device ID is duplicated.'})
        device.majors.add(
                Major.objects.get(
                    Q(jh__sj__univ__name=values.get('univ0')) &
                    Q(jh__name=values.get('jh0')) &
                    Q(name=values.get('major0'))
                    )
                )
        device.save()
        # Serialize
        serializer = UnivSerializer(Univ.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)
