from django.db.models import Q
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from univ.models import Univ, Major, Device
from univ.serializers import UnivSerializer, UnivListSerializer


class UnivList(APIView):
    def get(self, request):
        if not request.GET.get('id'):
            serializer = UnivListSerializer(Univ.objects.all(), many=True, context={'request':request})
            return Response(serializer.data)
        try:
            device = Device.objects.get(unique_id=request.GET.get('id'))
        except Device.DoesNotExist:
            return Response(
                    {'error': 'Device does not exist. To add a new device, use POST method.'},
                    status=status.HTTP_400_BAD_REQUEST,
                    )
        majors = device.majors.all()
        jhs = list(set([major.jh for major in majors]))
        sjs = list(set([major.jh.sj for major in majors]))
        univs = list(set([major.jh.sj.univ for major in majors])).order_by('name')
        serializer = UnivSerializer(univs, many=True, context={'request': request, 'sjs': sjs, 'jhs': jhs, 'majors': majors})
        return Response(serializer.data)

    def post(self, request):
        # Parameter existence check
        required_parameters = ['id', 'token', 'num']
        for param in required_parameters:
            if not param in request.data:
                return Response(
                        {'error': f'"{param}" parameter is required.'},
                        status=status.HTTP_400_BAD_REQUEST,
                        )
        num = int(request.data.get('num'))
        majors = []
        for i in range(num):
            majors.extend([f'univ{i}', f'jh{i}', f'major{i}'])
        for param in majors:
            if not param in request.data:
                return Response(
                        {'error': f'"{param}" parameter is required.'},
                        status=status.HTTP_400_BAD_REQUEST,
                        )
        # Create device info
        values = {param: request.data.get(param) for param in required_parameters}
        values.update({param: request.data.get(param) for param in majors})
        try:
            device = Device.objects.create(unique_id=values.get('id'), token=values.get('token'))
        except IntegrityError:
            Device.objects.get(unique_id=values.get('id')).delete()
            device = Device.objects.create(unique_id=values.get('id'), token=values.get('token'))
        for i in range(num):
            major = Major.objects.get(
                        Q(jh__sj__univ__name=values.get(f'univ{i}')) &
                        Q(jh__name=values.get(f'jh{i}')) &
                        Q(name=values.get(f'major{i}'))
                        )
            if major not in device.majors.all():
                device.majors.add(major)
        device.save()
        # Serialize
        serializer = UnivSerializer(Univ.objects.all(), many=True, context={'request': request})
        return Response(serializer.data)
