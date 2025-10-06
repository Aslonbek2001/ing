from rest_framework.views import APIView
from django.db.models import Prefetch
from rest_framework import generics
from menus.models import Menu
from menus.serializers.menu_serializers import MenuListSerializer, MenuDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Navbar and Menu"],
    summary="List and Create Menus",
    description=(
        "GET → Navbar’ni ichma-ich (nested) holda qaytaradi.\n"
        "POST → Yangi menyu qo‘shish imkonini beradi. \n"
    ),
)
class MenuListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  → Navbar ichma-ich olish (faqat parent bo‘lgan menyular)
    POST → Yangi menyu qo‘shish
    """
    # queryset = Menu.objects.filter(parent__isnull=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "parent"]  # Filtrlash imkoniyati
    serializer_class = MenuDetailSerializer

    def get_serializer_class(self):
        """GET uchun ListSerializer, POST uchun DetailSerializer"""
        if self.request.method == "GET":
            return MenuListSerializer
        return MenuDetailSerializer
    
    def get_queryset(self):
        """
        Auth → barcha menyular
        Anonymous → faqat status=True
        """
        base_qs = Menu.objects.only(
            "id", "title_uz", "title_ru", "title_en", "status", "position", "parent"
        ).filter(parent__isnull=True)

        # 🔥 Prefetch bolalar menyularini oldindan olish
        base_qs = base_qs.prefetch_related(
            Prefetch(
                "children",
                queryset=Menu.objects.only(
                    "id", "title_uz", "title_ru", "title_en", "status", "position", "parent"
                ).order_by("position")
            )
        )

        user = self.request.user
        if not user.is_authenticated:
            base_qs = base_qs.filter(status=True)

        return base_qs.order_by("position")
    




@extend_schema(
    tags=["Menu - Admin"],
    summary="Retrieve, Update, or Delete Menu",
    description=(
        "GET → Bitta menyuni olish\n"
        "PUT/PATCH → Menyuni yangilash\n"
        "DELETE → Menyuni o‘chirish"
    ),
)
class MenuDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"  # URL’da menu_id orqali topiladi
    lookup_url_kwarg = "menu_id"


# @extend_schema(tags=["Navbar and Menu"])
# class MenuListCreateAPIView(APIView):
#     """
#     GET  →  Navbar ichma ich olish 
#     POST →  Navbar qo'shish
#     """
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = MenuDetailSerializer
#     def get(self, request):
#         menus = Menu.objects.filter(parent__isnull=True, status=True)  # faqat bosh menyular
#         serializer = MenuListSerializer(menus, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(tags=["Menu - Admin"])
# class MenuDetailAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = MenuDetailSerializer
#     def get(self, request, menu_id):
#         page = get_object_or_404(Menu, id=menu_id)
#         serializer = self.serializer_class(page)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, menu_id):
#         page = get_object_or_404(Menu, id=menu_id)
#         serializer = self.serializer_class(page, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, menu_id):
#         page = get_object_or_404(Menu, id=menu_id)
#         page.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

