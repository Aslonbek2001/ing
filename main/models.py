from django.db import models


class Company(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    address_uz = models.TextField()
    address_ru = models.TextField()
    address_en = models.TextField()
    logo = models.ImageField(upload_to='company_logos/')
    stat_1 = models.IntegerField()
    stat_2 = models.IntegerField()
    stat_3 = models.IntegerField()
    stat_4 = models.IntegerField()
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    


    

