from django.contrib import admin
from .models import Profile, Region, BusinessInfo
# Register your models here.
admin.site.register(Profile)
admin.site.register(Region)
admin.site.register(BusinessInfo)