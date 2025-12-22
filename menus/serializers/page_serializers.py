from rest_framework import serializers
from menus.models import Page
from drf_spectacular.utils import extend_schema_field
from menus.models import Page
from menus.serializers.employee_serializers import EmployeeListSerializer
from menus.serializers.img_files_serializers import PageFileSerializer, PageImageSerializer
from menus.serializers.menu_serializers import MenuReadSerializer
from posts.serializers import PostManageListSerializer

# # # # # Default # # # # # 

class PageListSerializer(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)
    class Meta:
        model = Page
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    "status", "type", "slug", "menu"
                ]


class PageSerializer(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)

    class Meta:
        model = Page
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    'description_uz', 'description_ru', 'description_en',
                    "status", "type", "slug", "menu"
                ]
        read_only_fields = ['id']



# # # # # # Users # # # # 
class PageDetailSerializerForUsers(serializers.ModelSerializer):
    menu = MenuReadSerializer(read_only=True)
    images = PageImageSerializer(many=True, read_only=True)
    employees = EmployeeListSerializer(many=True, read_only=True)
    files = PageFileSerializer(many=True, read_only=True)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
                    "id", "menu",
                    'title_uz', 'title_ru', 'title_en',
                    'description_uz', 'description_ru', 'description_en',
                    "slug", "status", "images", "employees", "files", "posts"
                ]
    
    def get_posts(self, obj) -> list:
        try:
            if not obj.posts.exists():
                return []
        except:
            return []
        
        posts_qs = obj.posts.filter(status=True)
        return PostManageListSerializer(posts_qs, many=True).data



class PageListSerializerForUsers(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = [ "id", 'title_uz', 'title_ru', 'title_en']
        read_only_fields = ["id", "title_uz", "title_ru", "title_en"]



