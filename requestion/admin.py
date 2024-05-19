from django.contrib import admin
from .models import Requestion, Category, SubCategory,ReqImages
# used for importing and exporting of the data from the database
from import_export.admin import ImportExportModelAdmin

class Checkimpot(ImportExportModelAdmin, admin.ModelAdmin):
    pass

# The following three models can make use of import and export
admin.site.register(Category, Checkimpot)
admin.site.register(SubCategory, Checkimpot)
admin.site.register(Requestion, Checkimpot)
admin.site.register(ReqImages)