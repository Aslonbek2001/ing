from menus.models import Menu
from rest_framework import serializers

# # # # # # Users Admin # # # # # # #
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



# # # # # # Admin # # # # # # # 

class MenuDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = [
                    "id", 
                    'title_uz', 'title_ru', 'title_en',
                    "status", "position", "parent", ""
                ]

