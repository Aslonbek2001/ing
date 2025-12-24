from menus.models import Page
from menus.serializers.page_serializers import PageListSerializer, PageSerializer


class LabSer(PageListSerializer):
    class Meta(PageListSerializer.Meta):
        model = Page
        fields = list(PageListSerializer.Meta.fields) + ["position"]


class LabDetailSer(PageSerializer):
    class Meta(PageSerializer.Meta):
        model = Page
        fields = list(PageSerializer.Meta.fields) + ["position"]
