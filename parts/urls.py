from rest_framework.routers import DefaultRouter
from parts.views import CarouselViewSet


router = DefaultRouter()

router.register(r'carousels', CarouselViewSet, basename='carousel')

urlpatterns = router.urls