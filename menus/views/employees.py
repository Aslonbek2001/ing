from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from menus.models import Employee
from menus.serializers.employee_serializers import EmployeeDetailSerializer, EmployeeListSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from core.pagination import CustomPageNumberPagination


@extend_schema(tags=["Employees"])
class EmployeeListCreateAPIView(APIView):
    """
    GET  →  Barcha xodimlarni olish
    POST →  Yangi xodim yaratish
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EmployeeDetailSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        employees = Employee.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(employees, request)
        serializer = EmployeeListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Employees"])
class EmployeeDetailAPIView(APIView):
    """
    GET    →  Xodim ma'lumotlarini olish
    PUT    →  Xodimni yangilash
    DELETE →  Xodimni o‘chirish
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EmployeeDetailSerializer

    def get_object(self, employee_id):
        return get_object_or_404(Employee, id=employee_id)

    def get(self, request, employee_id):
        page = self.get_object(employee_id)
        serializer = self.serializer_class(page)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, employee_id):
        page = self.get_object(employee_id)
        serializer = self.serializer_class(page, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, employee_id):
        page = self.get_object(employee_id)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

