#!/usr/bin/python3
"""Other non default user related models script"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image #for image processing



class Region(models.Model):
    """A region model for user/requests profile"""
    name = models.CharField(max_length=45)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    """A model used for additional user informations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="avatar.jpg", upload_to="profile_pic")
    mobile = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    #BusinessInfo should not be deleted if region is deleted
    Region = models.ForeignKey(Region, default=None,
                               null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    
    def save(self,  *args, **kwargs):
        '''used for processing image before saving to the database'''
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            outpt = (300, 300)
            img.thumbnail(outpt)
            img.save(self.avatar.path)
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"


class BusinessInfo(models.Model):
    """A business identity model for users"""
    business_name = models.CharField(max_length=100)
    #BusinessInfo should not be deleted if region is deleted
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    subcity = models.CharField(max_length=45)
    TIN = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='business')
    renewed_licence = models.ImageField(upload_to="business")
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f"{ self.business_name }"
    
    def get_absolute_url(self):
        '''used to redirect to busines details after creating a new business'''
        return reverse("businessdetails", kwargs={"pk": str(self.pk)})