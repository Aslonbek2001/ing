from rest_framework.routers import DefaultRouter
from parts.views.carousel_view import CarouselViewSet
from parts.views.application_view import ApplicationViewSet


router = DefaultRouter()

router.register(r'carousels', CarouselViewSet, basename='carousel')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = router.urls