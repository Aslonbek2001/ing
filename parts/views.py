from .models import Carousel
from .serializers import CarouselSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Carousels"])
class CarouselViewSet(ModelViewSet):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

    def get_serializer_class(self):
        return CarouselSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)