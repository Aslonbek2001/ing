from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Post, PostImages
from .serializers import PostListSerializer, PostDetailSerializer, PostImageSerializer
from core.pagination import CustomPageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


@extend_schema(tags=["News & Announcements"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published_date")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "type"]
    search_fields = [
        "title_uz", "title_ru", "title_en"
    ]
    ordering_fields = ["published_date"]

    def get_queryset(self):
        qs = Post.objects.prefetch_related(
            Prefetch("images", queryset=PostImages.objects.only("id", "image"))
        )
        if self.action == "list":
            return qs.only(
                "id", "title_uz", "title_ru", "title_en", "image", "status", "published_date", "type"
            ).order_by("-published_date")
        return qs.order_by("-published_date")

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer


# ✅ Swagger uchun path parameterni aniqlab beramiz
@extend_schema(
    tags=["News & Announcements - Images"],
    parameters=[
        OpenApiParameter(
            name="post_pk",
            description="Parent Post ID",
            required=True,
            type=OpenApiTypes.INT,  # 👈 shu joy ogohlantirishni yo‘qotadi
            location=OpenApiParameter.PATH,
        )
    ],
)
class PostImageViewSet(viewsets.ModelViewSet):
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")  # url dan keladi
        post = get_object_or_404(Post, id=post_id)
        return post.images.all()


    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(post=post)


