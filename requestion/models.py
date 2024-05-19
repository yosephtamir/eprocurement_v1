from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from uuid import uuid4


class Category(models.Model):
    '''A catagory model used to specify a requests catagory information'''
    name = models.CharField(max_length=100, unique=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    '''More detailed specification of the catagory model'''
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcatagories')
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return self.name
    

class Requestion(models.Model):
    '''A requestion model to specify and save a proformas'''
    title = models.CharField(max_length=100)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='requestions')
    expirey_date = models.DateTimeField()
    location = models.CharField(max_length=150)
    unit = models.CharField(max_length=45)
    quantity = models.FloatField(max_length=10)
    details = models.TextField()
    sample = models.BooleanField(default=False)
    image = models.ImageField(default="requestion.jpg", null=True, upload_to="reqimages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requestions')
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        '''used to redirect to requestion detail'''
        return reverse("requestiondetails", kwargs={"pk": self.pk})

class ReqImages(models.Model):
    '''A model used to hold images of a requestion'''
    img = models.ImageField(default="licence.jpg", null=True, upload_to="reqimages")
    requestion = models.ForeignKey(Requestion, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return self.img