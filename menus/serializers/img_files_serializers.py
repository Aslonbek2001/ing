from menus.models import PageFiles, PageImages
from rest_framework import serializers



class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImages
        fields = ["id", "page", "image"]


class PageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageFiles
        fields = [
                    "id", "page",
                    'title_uz', 'title_ru', 'title_en',
                    "file", "position", "status"
                ]
