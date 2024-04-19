from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name
    
class Requestion(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    expirey_date = models.DateTimeField()
    location = models.CharField(max_length=150)
    unit = models.CharField(max_length=45)
    quantity = models.FloatField(max_length=10)
    details = models.TextField()
    image = models.ImageField(default="licence.jpg", null=True, upload_to="reqimages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("requestiondetails", kwargs={"pk": self.pk})

class ReqImages(models.Model):
    img = models.ImageField(default="licence.jpg", null=True, upload_to="reqimages")
    requestion = models.ForeignKey(Requestion, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.img