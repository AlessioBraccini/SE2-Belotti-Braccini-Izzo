from django.contrib import admin
from planningApp.models import *

# Register your models here.


class DailyPlanAdmin(admin.ModelAdmin):
    list_display = ('agronomist_user', 'date', 'visit_farmer')
admin.site.register(DailyPlan, DailyPlanAdmin)