from django.db import models


class Carousel(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='carousel/')
    description = models.TextField(blank=True, null=True, db_index=True)
    link = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title