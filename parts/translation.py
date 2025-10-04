from modeltranslation.translator import register, TranslationOptions
from .models import Carousel

@register(Carousel)
class CarouselTranslationOptions(TranslationOptions):
    fields = ("title", "description")
