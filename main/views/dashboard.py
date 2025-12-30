from menus.models import Page, Menu, Employee, PageFiles
from parts.models import Carousel, Application
from posts.models import Post, PostImages
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from main.serializers import DashboardSerializer
from main.service import DashboardService

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSerializer

    @extend_schema(
        tags=["Dashboard"],
        description="Dashboard uchun umumiy statistik ma'lumotlar (nomi va soni).",
    )
    def get(self, request, *args, **kwargs):
        serializers = DashboardService.get_dashboard_data()
        return Response(
            serializers.data, status=200
        )
