from django.db import models
from django.utils.text import slugify


class Menu(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )
    status = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Page(models.Model):
    PAGE_TYPES = (
        ('department', 'Bo‘lim'),
        ('faculty', 'Kafedra'),
        ('lab', 'Laboratoriya'),
        ('page', 'Sahifa'),
    )
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=PAGE_TYPES, default='page')
    menu = models.OneToOneField(
        Menu,
        on_delete=models.CASCADE,
        related_name='page',
        null=True, blank=True
    )
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.menu:
                self.slug = slugify(self.title)
            else: self.slug = slugify(self.menu.title)

        super().save(*args, **kwargs)


class PageImages(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Paga tegishli rasm"
    )
    image = models.ImageField(
        upload_to="page_images/",
        help_text="Rasm"
    )

    class Meta:
        db_table = "page_images"
        verbose_name = "Post Rasmi"
        verbose_name_plural = "Post Rasmlari"

    def __str__(self):
        return f"Post: {self.page.title} - Rasm ID: {self.id}"


class Employee(models.Model):
    full_name = models.CharField(max_length=200, db_index=True,)
    position = models.CharField(max_length=200, db_index=True,)
    description = models.TextField(blank=True, null=True)
    pages = models.ManyToManyField(
        Page,
        related_name="employees",
        db_index=True,
        blank=True
    )
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class PageFiles(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="files",
        help_text="Fayl tegishli xodim"
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(
        upload_to="employee_files/",
        help_text="Fayl"
    )
    position = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "page_files"
        verbose_name = "Page Fayli"
        verbose_name_plural = "Page Fayllari"

    def __str__(self):
        return f"Page: {self.page.title} - Fayl ID: {self.id}"