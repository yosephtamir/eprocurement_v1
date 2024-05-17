from django.contrib import admin
from .models import Profile, Region, BusinessInfo
from import_export.admin import ImportExportModelAdmin
class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Region, Checkimpot)
admin.site.register(Profile)
admin.site.register(BusinessInfo)