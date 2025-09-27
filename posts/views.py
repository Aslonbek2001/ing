from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer
from core.pagination import CustomPageNumberPagination # agar sizda custom pagination bo‘lsa


@extend_schema(tags=["News & Announcements"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published_date")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["status", "type"]
    search_fields = [
        "title_uz", "title_ru", "title_en",
        "description_uz", "description_ru", "description_en",
    ]
    ordering_fields = ["published_date"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer
