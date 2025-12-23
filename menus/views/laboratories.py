from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import generics, status
from menus.services.page_services import PageService
from menus.models import Page
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from core.pagination import CustomPageNumberPagination
from menus.serializers.page_serializers import (
    PageDetailSerializerForUsers, PageListSerializer, 
    PageSerializer, PageListSerializerForUsers
)

@extend_schema(
    tags=["Admin - Page"],
    summary="List and Create Pages",
    description="Allows admin users to list all pages or create a new page.",
    parameters=[
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=[choice[0] for choice in Page.PAGE_TYPES],
            description="Filter pages by type.",
        ),
    ],
)
class PageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "menu", "title", "type"]
    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PageListSerializer
        return PageSerializer


@extend_schema(
    tags=["Admin - Page"],
    summary="Retrieve, Update, or Delete a Page",
    description="Retrieve, partially update, or delete a specific page by slug.",
)
class PageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(status=True)
        return Page.objects.all()
    
