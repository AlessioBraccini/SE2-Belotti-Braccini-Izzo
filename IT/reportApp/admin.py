from django.contrib import admin
from .models import *

# Register your models here.


class SteeringInitiativesAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'title')
admin.site.register(SteeringInitiative, SteeringInitiativesAdmin)
