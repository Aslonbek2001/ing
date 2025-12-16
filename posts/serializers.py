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


class PostManageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title_uz", "title_ru", "title_en", "image"]
        read_only_fields = ["id"]

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None


class PostManageSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    remove_image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "status", "published_date", "type",
            "images", "upload_images", "remove_image_ids"
        ]
        read_only_fields = ["id", "images"]

    def create(self, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        post = Post.objects.create(**validated_data)
        self._create_images(post, upload_images)
        return post

    def update(self, instance, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        remove_ids = validated_data.pop("remove_image_ids", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if remove_ids:
            instance.images.filter(id__in=remove_ids).delete()

        self._create_images(instance, upload_images)
        return instance

    def _create_images(self, post, images):
        for image in images:
            PostImages.objects.create(post=post, image=image)

