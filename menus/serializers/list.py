from menus.models import Menu, PageImages, Employee, PageFiles
from rest_framework import serializers



class MenuListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    page_slug = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    "status", "position", "page_slug", "children"
                ]

    def get_page_slug(self, obj):
        if hasattr(obj, 'page') and obj.page:
            return obj.page.slug
        return None
    
    
    def get_children(self, obj):
        return MenuListSerializer(obj.children.all(), many=True).data



class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "order",
                    "phone", "email", "photo"
                ]


class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImages
        fields = ["id", "image"]


class PageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageFiles
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en', 
                    "file", "position", "status"
                ]