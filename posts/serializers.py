from rest_framework import serializers
from .models import Post, PostImages

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['id', 'image']
        read_only_fields = ['id']


class PostListSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None
    
    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "status", "published_date", "type", "image"
        ]
        read_only_fields = ["id"]
    

class PostCreateSerializer(serializers.ModelSerializer):

    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "status", "published_date", "type", "upload_images"
        ]
        read_only_fields = ["id"]
    
    def create(self, validated_data):
        upload_images = validated_data.pop('upload_images', [])
        post = Post.objects.create(**validated_data)
        for image in upload_images:
            PostImages.objects.create(post=post, image=image)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "status", "published_date", "type", "images"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title_uz": {"required": True},
            "description_uz": {"required": True},
        }


