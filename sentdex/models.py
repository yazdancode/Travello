from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone



from django.db import models

class Destination(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='شناسه')
    country = models.CharField(max_length=256, verbose_name='کشور')
    img1 = models.ImageField(upload_to='pics', verbose_name='تصویر یک')
    img2 = models.ImageField(upload_to='pics', verbose_name='تصویر دو')
    number = models.IntegerField(default=2, verbose_name='شماره')

    class Meta:
        verbose_name = "مقصد"
        verbose_name_plural = "مقصد"
        
    def __str__(self):
        return f"Destination {self.id} - {self.country}"
    
    
class Detailed_desc(models.Model):
    pass
    