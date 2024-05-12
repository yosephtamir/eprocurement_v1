from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import BusinessInfo
from requestion.models import Requestion
from django.urls import reverse
from django_cryptography.fields import encrypt



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.ImageField(default="blog.jpg", upload_to="blog")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"({self.id}) {self.title}"
    
class Proforma(models.Model):
    requestion = models.ForeignKey(Requestion, on_delete=models.CASCADE)
    #I wanted to keep the proforma even if the user is deleted.
    #But it is not going to reference the user name
    #what can I do?
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    business = models.ForeignKey(BusinessInfo, null=True, on_delete=models.SET_NULL)
    
    price = encrypt(models.CharField(max_length=255))
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.requestion.title}'
    
    def get_absolute_url(self):
        return reverse("requestionlist")