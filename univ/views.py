from rest_framework import generics

from univ.models import Univ
from univ.serializers import UnivSerializer


class UnivList(generics.ListAPIView):
    queryset = Univ.objects.all()
    serializer_class = UnivSerializer

