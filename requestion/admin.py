from django.contrib import admin
from .models import Requestion, Category, SubCategory,ReqImages
from import_export.admin import ImportExportModelAdmin

class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Category, Checkimpot)
admin.site.register(SubCategory, Checkimpot)
admin.site.register(Requestion, Checkimpot)
admin.site.register(ReqImages)