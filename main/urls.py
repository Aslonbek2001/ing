
from django.urls import path
from main.views.main_view import HomePageView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home-page'),
]
