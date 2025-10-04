from parts.models import Carousel
from rest_framework import serializers


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    'description_uz', 'description_ru', 'description_en',
                    "image", "link", "position", "status"
                ]
        read_only_fields = ["id"]
