#!/usr/bin/python3
"""Used to make the models available to the admin site"""
from django.contrib import admin
from .models import Profile, Region, BusinessInfo
from import_export.admin import ImportExportModelAdmin


class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    # used easy import and export of the region model
    pass

admin.site.register(Region, Checkimpot)
admin.site.register(Profile)
admin.site.register(BusinessInfo)