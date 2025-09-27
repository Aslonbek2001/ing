from django.db import models
from versatileimagefield.fields import VersatileImageField
from core.mixins import auto_delete_image_with_renditions

type_choices = (
    ("news", "Yangilik"),
    ("announcement", "E'lon"),
)

# Create your models here.
class Post(models.Model):
    
    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Sarlavha"
    )
    image = VersatileImageField(
        upload_to="posts/",
        null=True,
        blank=True,
        help_text="Rasm (ixtiyoriy)"
    )
    description = models.TextField(
        help_text="Batafsil ma'lumot"
    )
    status = models.BooleanField(
        default=True,
        help_text="Aktiv yoki yo'q"
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        help_text="E'lon qilingan sana"
    )
    type = models.CharField(
        max_length=20,
        choices=type_choices,
        default="news",
        help_text="Turini tanlang"
    )

    class Meta:
        db_table = "posts"
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
            models.Index(fields=["published_date"]),
        ]
        verbose_name = "Post (Yangilik/E'lon)"
        verbose_name_plural = "Postlar (Yangiliklar va E'lonlar)"

    def __str__(self):
        return f"{self.title}"

auto_delete_image_with_renditions(Post, "image")