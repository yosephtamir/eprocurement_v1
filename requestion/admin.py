from django.contrib import admin
from .models import Requestion, Category, SubCategory,ReqImages
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Requestion)
admin.site.register(ReqImages)