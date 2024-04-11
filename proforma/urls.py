from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Blog"),
    path('about/', views.about, name="Proforma-About"),
]
