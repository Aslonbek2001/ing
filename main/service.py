from parts.models import Application, Carousel
from menus.models import Menu, Page, PageImages, PageFiles, Employee
from parts.serializers import ApplicationSerializer, CarouselSerializer
from menus.serializers.employee_serializers import EmployeeListSerializer, EmployeeDetailSerializer



class HomePageService:
    @staticmethod
    def get_carusels():
        carousels = Carousel.objects.filter(status=True).order_by("position")
        serializer = CarouselSerializer(carousels, many=True)
        return serializer.data
    
    @staticmethod
    def get_()
        pass


