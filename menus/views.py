from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Menu, Page
from menus.serializers.list import MenuListSerializer
from menus.serializers.detail import PageDetailSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Users - Navbar"])
class MenuListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MenuListSerializer
    def get(self, request):
        menus = Menu.objects.filter(parent__isnull=True, status=True)  # faqat bosh menyular
        serializer = MenuListSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@extend_schema(tags=["Users - Page"])
class PageDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PageDetailSerializer
    def get(self, request, slug):
        page = get_object_or_404(Page, slug=slug, status=True)
        serializer = self.serializer_class(page)
        return Response(serializer.data, status=status.HTTP_200_OK)











# @extend_schema(tags=["Pages"])
# class PageDetailAPIView(APIView):
#     def get(self, request, slug):
#         page = get_object_or_404(Page, slug=slug, status=True)
#         serializer = PageSerializer(page)
#         return Response(serializer.data, status=status.HTTP_200_OK)


