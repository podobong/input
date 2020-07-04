from django.db.models import Q
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from univ.models import Univ, Major, Device
from univ.serializers import UnivSerializer


class UnivList(APIView):
    def get(self, request):
        # Parameter existence check
        if not 'id' in request.GET:
            return Response(
                    {'error': '"id" parameter is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                    )
        # Serialize
        serializer = UnivSerializer(Univ.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Parameter existence check
        required_parameters = ('id', 'univ', 'jh', 'major')
        for param in required_parameters:
            if not param in request.GET:
                return Response(
                        {'error': f'"{param}" parameter is required.'},
                        status=status.HTTP_400_BAD_REQUEST,
                        )
        # Create device info
        values = {param: request.GET.get(param) for param in required_parameters}
        try:
            device = Device.objects.create(unique_id=values.get('id'))
        except IntegrityError:
            return Response({'error': 'Device ID is duplicated.'})
        device.majors.add(
                Major.objects.get(
                    Q(jh__sj__univ__name=values.get('univ')) &
                    Q(jh__name=values.get('jh')) &
                    Q(name=values.get('major'))
                    )
                )
        device.save()
        # Serialize
        serializer = UnivSerializer(Univ.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)

