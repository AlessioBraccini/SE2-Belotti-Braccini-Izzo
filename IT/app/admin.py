from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *


# Register your models here.

class FarmAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'score', 'visit_ctr')
admin.site.register(Farm, FarmAdmin)


class CropAdmin(admin.ModelAdmin):
    list_display = ('farm', 'crop_type')
admin.site.register(Crop, CropAdmin)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop_type', 'qty_sown', 'sown_date', 'qty_harvested', 'harvested_date')
admin.site.register(Production, ProductionAdmin)



