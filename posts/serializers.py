from rest_framework import serializers
from menus.models import Page
from .models import Post, PostImages

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['id', 'image']
        read_only_fields = ['id']


class PostManageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    pages = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ["id", "title_uz", "title_ru", "title_en", "image", "pages"]
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
    pages = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            "id", "title_uz", "title_ru", "title_en",
            "description_uz", "description_ru", "description_en",
            "status", "published_date", "type", "pages",
            "images", "upload_images", "remove_image_ids"
        ]
        read_only_fields = ["id", "images"]

    def create(self, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        pages = validated_data.pop("pages", [])
        post = Post.objects.create(**validated_data)
        if pages:
            post.pages.set(pages)
        self._create_images(post, upload_images)
        return post

    def update(self, instance, validated_data):
        upload_images = validated_data.pop("upload_images", [])
        remove_ids = validated_data.pop("remove_image_ids", [])
        pages = validated_data.pop("pages", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if pages is not None:
            instance.pages.set(pages)

        if remove_ids:
            instance.images.filter(id__in=remove_ids).delete()

        self._create_images(instance, upload_images)
        return instance

    def _create_images(self, post, images):
        for image in images:
            PostImages.objects.create(post=post, image=image)
