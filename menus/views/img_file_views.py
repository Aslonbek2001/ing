from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from menus.models import Page
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from menus.serializers.img_files_serializers import PageImageSerializer, PageFileSerializer
from menus.models import PageFiles, PageImages



@extend_schema(
    tags=["Admin - Page Files"],
    summary="List and Create Page Files",
    description=(
        "GET → Sahifa fayllarini ro‘yxatini olish (filter, search, ordering bilan)\n"
        "POST → Yangi fayl qo‘shish"
    ),
)
class PageFileListCreateAPIView(generics.ListCreateAPIView):
    queryset = PageFiles.objects.all()
    serializer_class = PageFileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 🔍 Filter, Search, Ordering backendlari
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 🧩 Filtrlash uchun maydonlar
    filterset_fields = ["page", "status", "position"]

    # 🔎 Qidirish uchun maydonlar
    search_fields = ["title_uz", "title_ru", "title_en"]

    # ↕️ Tartiblash uchun maydonlar
    ordering_fields = ["position", "id", "title_uz"]

    # Default ordering
    ordering = ["position"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return self.queryset.filter(status=True)
        return self.queryset
    
    def get_serializer_context(self):
        return {}

    
@extend_schema(
    tags=["Admin - Page Files"],
    summary="Retrieve, Update, or Delete Page File",
    description=(
        "GET → Bitta fayl ma'lumotini olish\n"
        "PUT/PATCH → Faylni yangilash\n"
        "DELETE → Faylni o‘chirish"
    ),
)
class PageFileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageFiles.objects.all()
    serializer_class = PageFileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_serializer_context(self):
        return {}


@extend_schema(
    tags=["Admin - Page Images"],
    summary="List and Create Page Images",
    description=(
        "GET → Sahifa rasmlarini ro‘yxatini olish (filter, search, ordering bilan)\n"
        "POST → Yangi rasm qo‘shish"
    ),
)
class PageImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = PageImages.objects.all()
    serializer_class = PageImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["page"]
    ordering_fields = ["id"]
    ordering = ["-id"]

    def get_serializer_context(self):
        return {}


@extend_schema(
    tags=["Admin - Page Images"],
    summary="Retrieve, Update, or Delete Page Image",
    description=(
        "GET → Bitta rasmni olish\n"
        "PUT/PATCH → Rasmni yangilash\n"
        "DELETE → Rasmni o‘chirish"
    ),
)
class PageImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PageImages.objects.all()
    serializer_class = PageImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def get_serializer_context(self):
        return {}
