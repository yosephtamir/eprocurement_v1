#!/usr/bin/python3
"""A proforma/procurement model"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import BusinessInfo
from requestion.models import Requestion
from django.urls import reverse
from django_cryptography.fields import encrypt



class Post(models.Model):
    '''A model used for blog posts'''
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.ImageField(default="blog.jpg", upload_to="blog")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self):
        return f"({self.id}) {self.title}"
    
class Proforma(models.Model):
    """A proforma model
        ***The user should be kept even if it is deleted but,
        in this case it is going to be null***"""
    requestion = models.ForeignKey(Requestion, on_delete=models.CASCADE,
                                   related_name='proformas')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             related_name='proformas')
    business = models.ForeignKey(BusinessInfo, null=True, on_delete=models.SET_NULL)
    price = encrypt(models.CharField(max_length=255)) #price should be encryptd
    additional_infos = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self):
        return f'{self.requestion.title}'
    
    def get_absolute_url(self):
        return reverse("requestionlist") 