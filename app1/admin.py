from django.contrib import admin

from .models import tanks,marker,booster,jw,wtp

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

# Register your models here.


@admin.register(marker)
class markerAdmin(ImportExportModelAdmin):
    pass


@admin.register(tanks)
class tanksAdmin(ImportExportModelAdmin):
    pass


@admin.register(booster)
class boosterAdmin(ImportExportModelAdmin):
    pass

@admin.register(jw)
class jwAdmin(ImportExportModelAdmin):
    pass

@admin.register(wtp)
class wtpAdmin(ImportExportModelAdmin):
    pass

# @admin.register(tanks)
# class tanks(ImportExportModelAdmin):
#     pass

# # class tankResource(resources.ModelResource):

# #     class Meta:
# #         model = tanks

# admin.site.register(marker)