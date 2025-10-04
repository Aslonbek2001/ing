from modeltranslation.translator import register, TranslationOptions
from .models import Page, Menu, Employee, PageFiles

@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Page)
class PostTranslationOptions(TranslationOptions):
    fields = ("title", "description")

@register(Employee)
class PostTranslationOptions(TranslationOptions):
    fields = ("full_name", "position", "description")

@register(PageFiles)
class PostTranslationOptions(TranslationOptions):
    fields = ("title",)