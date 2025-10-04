from django.urls import path
from .views import MenuListAPIView, PageDetailAPIView

urlpatterns = [
    path("menus/", MenuListAPIView.as_view(), name="menu-list"),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view(), name="page-detail"),
]
