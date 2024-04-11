from django.shortcuts import render
from django.http import HttpResponse
from .models import Post




def home(request):
    context = {
         "posts": Post.objects.all()
    }
    return render(request, "proforma/home.html", context)
def about(request):
     return render(request, "proforma/about.html")

# Create your views here.
