from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    '''A project model used as projects and initiatives data holder'''
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.ImageField(default="projects.jpg", upload_to="projects")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self):
        return f"({self.id}) {self.title}"