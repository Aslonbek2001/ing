from django.urls import path
from menus.views.menus import MenuListCreateAPIView, MenuDetailAPIView
from menus.views.pages import PageListCreateAPIView, PageDetailAPIView, PageDetailForUsers
from menus.views.employees import EmployeeListCreateAPIView, EmployeeDetailAPIView
from menus.views.img_file_views import PageFileDetailAPIView, PageFileListCreateAPIView, PageImageDetailAPIView, PageImageListCreateAPIView

urlpatterns = [
    # Menus
    path("menus/", MenuListCreateAPIView.as_view(), name="menu-list-create"),
    path("menus/<int:menu_id>/", MenuDetailAPIView.as_view(), name="menu-detail"),

    # Pages
    path("pages-users/<slug:slug>/", PageDetailForUsers.as_view(), name="page-for-users"),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view(), name="page-detail"),
    path("pages/", PageListCreateAPIView.as_view(), name="page-list-create"),

    # 🗂 Page Files
    path("page-files/", PageFileListCreateAPIView.as_view(), name="page-file-list-create"),
    path("page-files/<int:id>/", PageFileDetailAPIView.as_view(), name="page-file-detail"),

    # 🖼 Page Images
    path("page-images/", PageImageListCreateAPIView.as_view(), name="page-image-list-create"),
    path("page-images/<int:id>/", PageImageDetailAPIView.as_view(), name="page-image-detail"),

    


    # Employees
    path("employees/", EmployeeListCreateAPIView.as_view(), name="employee-list-create"),
    path("employees/<int:employee_id>/", EmployeeDetailAPIView.as_view(), name="employee-detail")


]
