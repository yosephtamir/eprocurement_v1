from typing import Iterable
from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse

class Region(models.Model):
    name = models.CharField(max_length=45)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="avatar.jpg", upload_to="profile_pic")
    #BusinessInfo should not be deleted if region is deleted
    Region = models.ForeignKey(Region, default=None, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self):
        super().save()
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            outpt = (300, 300)
            img.thumbnail(outpt)
            img.save(self.avatar.path)
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"


class BusinessInfo(models.Model):
    business_name = models.CharField(max_length=100)
    #BusinessInfo should not be deleted if region is deleted
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    subcity = models.CharField(max_length=45)
    TIN = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    renewed_licence = models.ImageField(default="licence.jpg", upload_to="business")
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{ self.user.username }'s Business"
    
    def get_absolute_url(self):
        reverse('Blog')