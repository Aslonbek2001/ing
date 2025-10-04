from rest_framework import serializers
from menus.models import Page, Menu, PageImages, Employee, PageFiles
from drf_spectacular.utils import extend_schema_field
from menus.serializers.list import (
            EmployeeListSerializer, PageImageSerializer, 
            EmployeeListSerializer, PageFileSerializer
        )



# # # # # # Users # # # # 
class PageDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    employees = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ["id", "title", "slug", "status", "description", "images", "employees", "files"]

    @extend_schema_field(PageImageSerializer(many=True))
    def get_images(self, obj):
        if hasattr(obj, 'images'):
            return PageImageSerializer(obj.images.all(), many=True).data
        return None

    @extend_schema_field(EmployeeListSerializer(many=True))
    def get_employees(self, obj):
        if hasattr(obj, 'employees'):
            return EmployeeListSerializer(obj.employees.all(), many=True).data
        return None
    
    @extend_schema_field(PageFileSerializer(many=True))
    def get_files(self, obj):
        if hasattr(obj, 'files'):
            return PageFileSerializer(obj.files.all(), many=True).data
        return None


# # # # # # Admin # # # # # # # 

class MenuDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ["id", "title", "status", "position"]
    
    
    def get_children(self, obj):
        return MenuDetailSerializer(obj.children.all(), many=True).data
