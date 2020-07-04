from django.db.models import Q
from django.db import IntegrityError
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from univ.models import Univ, Major, Device
from univ.serializers import UnivSerializer


class UnivList(generics.ListAPIView):
    queryset = Univ.objects.all()
    serializer_class = UnivSerializer


class DeviceInfo(APIView):
    def get(self, request):
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
        device = Device.objects.create(unique_id=values.get('id'))
        device.majors.add(
                Major.objects.get(
                    Q(jh__sj__univ__name=values.get('univ')) &
                    Q(jh__name=values.get('jh')) &
                    Q(name=values.get('major'))
                    )
                )
        # Device duplication check & save
        try:
            device.save()
        except IntegrityError:
            return Response({'error': 'Device ID is duplicated.'})
        return Response({'success': 'Successfully saved data.'})

