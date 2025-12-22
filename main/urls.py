
from django.urls import path
from main.views.main_view import HomePageView
from main.views.full_search import FullSearchAPIView
from main.views.company_view import CompanyAPIView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home-page'),
    path('search/', FullSearchAPIView.as_view(), name='full-search'),
    path('company/', CompanyAPIView.as_view(), name='company'),
]
