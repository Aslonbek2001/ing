from parts.models import Carousel
from rest_framework import serializers


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ["id", "title", "image", "description", "link", "position", "status"]
        read_only_fields = ["id"]
