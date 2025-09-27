from rest_framework import serializers
from .models import Post
from versatileimagefield.serializers import VersatileImageFieldSerializer

class PostListSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "image", "status", "published_date", "type"
        ]
        read_only_fields = ["id"]
    
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            try:
                return request.build_absolute_uri(obj.image.thumbnail['400x400'].url)  # medium variant
            except Exception:
                return obj.image.url  # fallback original
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id",
            "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "image", "status", "published_date", "type",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title_uz": {"required": True},
            "description_uz": {"required": True},
        }
        
    # def get_image(self, obj):
    #     request = self.context.get("request")
    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)  # faqat original
    #     return None