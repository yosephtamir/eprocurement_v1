from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from requestion.models import Requestion

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return f"({self.id}) {self.title}"
    
class Proforma(models.Model):
    requestion = models.ForeignKey(Requestion, on_delete=models.CASCADE)
    #I wanted to keep the proforma even if the user is deleted.
    #But it is not going to reference the user name
    #what can I do?
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    price = models.FloatField(editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.requestion.title}'