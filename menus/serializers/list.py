from menus.models import Menu, Page, PageImages, Employee, PageFiles
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class MenuListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    page_slug = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "title", "status", "position", "page_slug", "children"]

    def get_page_slug(self, obj):
        if hasattr(obj, 'page') and obj.page:
            return obj.page.slug
        return None
    
    
    def get_children(self, obj):
        return MenuListSerializer(obj.children.all(), many=True).data



class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "phone", "email", "photo"]


class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImages
        fields = ["id", "image"]


class PageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageFiles
        fields = ["id", "title", "file", "position", "status"]