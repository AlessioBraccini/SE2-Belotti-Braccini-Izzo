from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(Farm)
admin.site.register(Crop)
admin.site.register(Production)
admin.site.register(DailyPlan)
admin.site.register(HelpRequest)
admin.site.register(SteeringInitiative)
