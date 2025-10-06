from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from menus.services.page_services import PageService
from menus.models import Page, PageImages, PageFiles, Employee
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from menus.serializers.page_serializers import (
    PageDetailSerializerForUsers, PageListSerializer, PageSerializer
)


@extend_schema( tags=["Users - Page"])
class PageDetailForUsers(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PageDetailSerializerForUsers
    def get(self, request, slug):
        page = PageService.get_page_by_slug_for_users(slug)
        serializer = self.serializer_class(page)
        return Response(serializer.data, status=status.HTTP_200_OK)




# ===============================
# 📋 ADMIN - Page List & Create
# ===============================
@extend_schema(
    tags=["Admin - Page"],
    summary="List and Create Pages",
    description="Allows admin users to list all pages or create a new page.",
)
class PageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "menu", "title"]
    serializer_class = PageSerializer

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
    lookup_field = "slug"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Page.objects.filter(status=True)
        return Page.objects.all()


# @extend_schema(tags=["Admin - Page"], operation_id="page-list-create")
# class PageListCreateAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PageSerializer

#     def get(self, request):
#         pages = Page.objects.all()
#         serializer = PageListSerializer(pages, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(tags=["Admin - Page"], operation_id="page-detail-for-admin")
# class PageDetailAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PageSerializer
#     def get(self, request, slug):
#         page = get_object_or_404(Page, slug=slug, status=True)
#         serializer = self.serializer_class(page)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, slug):
#         page = get_object_or_404(Page, slug=slug, status=True)
#         serializer = self.serializer_class(page, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, slug):
#         page = get_object_or_404(Page, slug=slug, status=True)
#         page.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
