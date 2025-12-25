from menus.models import Page
from menus.serializers.page_serializers import PageListSerializer, PageSerializer


class DepartmentListSerializer(PageListSerializer):
    class Meta(PageListSerializer.Meta):
        model = Page
        fields = list(PageListSerializer.Meta.fields) + [
            "sub_title",
            "position",
        ]


class DepartmentSerializer(PageSerializer):
    class Meta(PageSerializer.Meta):
        model = Page
        fields = list(PageSerializer.Meta.fields) + [
            "sub_title",
            "position",
        ]
