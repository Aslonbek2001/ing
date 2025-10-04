from django.contrib import admin
from .models import Carousel
# Register your models here.

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'position')
    list_editable = ('status', 'position')
    search_fields = ('title',)
    list_filter = ('status',)