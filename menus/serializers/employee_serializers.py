from rest_framework import serializers
from menus.models import  Employee

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "order",
                    "phone", "email", "image"
                ]

class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "description_uz", "description_ru", "description_en",
                    "order",
                    "phone", "email", "image"
                ]
        

