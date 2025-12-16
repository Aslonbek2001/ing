from main.models import Company
from posts.models import Post
from parts.models import Carousel
from menus.models import Page
from menus.models import Menu



class HomePageService:
    
    @staticmethod
    def get_navbar():
        return Menu.objects.filter(parent__isnull=True, status=True).order_by('position')
        

    @staticmethod
    def get_carousels():
        return Carousel.objects.filter(status=True).order_by('position')

    @staticmethod
    def get_company_info():
        return Company.objects.first()
    
    @staticmethod
    def get_latest_posts():
        return Post.objects.filter(status=True).order_by('-published_date')[:6]

    @staticmethod
    def scientific_directions():
        return Page.objects.filter(type="scientific_direction").order_by("menu__position")

    @staticmethod
    def postgraduate_education():
        return Page.objects.filter(type="postgraduate_education").order_by("menu__position")
    


