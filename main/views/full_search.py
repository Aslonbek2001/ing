from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from menus.models import Employee, Menu, Page, PageFiles
from posts.models import Post
from parts.models import Carousel


@extend_schema(
    tags=["Search"],
    description="Project bo'yicha umumiy qidiruv.",
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Qidiruv matni.",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Har bir model uchun maksimal natija (default: 10).",
        ),
    ],
)
class FullSearchAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = (request.query_params.get("q") or "").strip()
        if not query:
            return Response(
                {
                    "query": query,
                    "results": {
                        "menus": [],
                        "pages": [],
                        "posts": [],
                        "employees": [],
                        "page_files": [],
                        "carousels": [],
                    },
                }
            )

        try:
            limit = int(request.query_params.get("limit", 10))
        except (TypeError, ValueError):
            limit = 10
        limit = max(1, min(limit, 50))

        is_auth = request.user.is_authenticated

        def with_status(qs):
            if is_auth:
                return qs
            return qs.filter(status=True)

        menus = with_status(
            Menu.objects.filter(
                Q(title_uz__icontains=query)
                | Q(title_ru__icontains=query)
                | Q(title_en__icontains=query)
            )
        ).values("id", "title_uz", "title_ru", "title_en", "status")[:limit]

        pages = with_status(
            Page.objects.filter(
                Q(title_uz__icontains=query)
                | Q(title_ru__icontains=query)
                | Q(title_en__icontains=query)
                | Q(description_uz__icontains=query)
                | Q(description_ru__icontains=query)
                | Q(description_en__icontains=query)
            )
        ).values(
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "type",
            "slug",
            "status",
        )[:limit]

        posts = with_status(
            Post.objects.filter(
                Q(title_uz__icontains=query)
                | Q(title_ru__icontains=query)
                | Q(title_en__icontains=query)
                | Q(description_uz__icontains=query)
                | Q(description_ru__icontains=query)
                | Q(description_en__icontains=query)
            )
        ).values(
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "published_date",
            "type",
            "status",
        )[:limit]

        employees = with_status(
            Employee.objects.filter(
                Q(full_name_uz__icontains=query)
                | Q(full_name_ru__icontains=query)
                | Q(full_name_en__icontains=query)
                | Q(position_uz__icontains=query)
                | Q(position_ru__icontains=query)
                | Q(position_en__icontains=query)
                | Q(description_uz__icontains=query)
                | Q(description_ru__icontains=query)
                | Q(description_en__icontains=query)
            )
        ).values(
            "id",
            "full_name_uz",
            "full_name_ru",
            "full_name_en",
            "position_uz",
            "position_ru",
            "position_en",
            "status",
        )[:limit]

        page_files = with_status(
            PageFiles.objects.filter(
                Q(title_uz__icontains=query)
                | Q(title_ru__icontains=query)
                | Q(title_en__icontains=query)
            )
        ).values("id", "title_uz", "title_ru", "title_en", "status")[:limit]

        carousels = with_status(
            Carousel.objects.filter(
                Q(title_uz__icontains=query)
                | Q(title_ru__icontains=query)
                | Q(title_en__icontains=query)
                | Q(description_uz__icontains=query)
                | Q(description_ru__icontains=query)
                | Q(description_en__icontains=query)
            )
        ).values("id", "title_uz", "title_ru", "title_en", "status")[:limit]

        return Response(
            {
                "query": query,
                "limit": limit,
                "results": {
                    "menus": list(menus),
                    "pages": list(pages),
                    "posts": list(posts),
                    "employees": list(employees),
                    "page_files": list(page_files),
                    "carousels": list(carousels),
                },
            }
        )
