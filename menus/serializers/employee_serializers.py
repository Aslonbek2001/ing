from rest_framework import serializers
from menus.models import Employee, Page

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "order", "pages",
                    "phone", "email", "image"
                ]



class EmployeeDetailSerializer(serializers.ModelSerializer):
    pages = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Employee
        fields = [
                    "id", 
                    "full_name_uz", "full_name_ru", "full_name_en",
                    "position_uz", "position_ru", "position_en",
                    "description_uz", "description_ru", "description_en",
                    "order", "pages",
                    "phone", "email", "image"
                ]

    def to_internal_value(self, data):
        data = data.copy()
        pages = data.get("pages")
        if hasattr(data, "getlist"):
            pages = data.getlist("pages") or pages
        if isinstance(pages, str):
            data["pages"] = [p.strip() for p in pages.split(",") if p.strip()]
        elif isinstance(pages, list):
            normalized = []
            for item in pages:
                if isinstance(item, str) and "," in item:
                    normalized.extend([p.strip() for p in item.split(",") if p.strip()])
                    continue
                if isinstance(item, dict) and "id" in item:
                    normalized.append(item["id"])
                elif isinstance(item, (list, tuple)):
                    normalized.extend(item)
                else:
                    normalized.append(item)
            data["pages"] = normalized
        return super().to_internal_value(data)

    def create(self, validated_data):
        pages = validated_data.pop("pages", [])
        employee = Employee.objects.create(**validated_data)
        if pages:
            employee.pages.set(pages)
        return employee
    
    def update(self, instance, validated_data):
        pages = validated_data.pop("pages", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if pages is not None:
            instance.pages.set(pages)
        return instance
        
