from django.contrib import admin
from .models import *

# Register your models here.


class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'date', 'subject')
admin.site.register(HelpRequest, HelpRequestAdmin)
