from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *


# Register your models here.
admin.site.register(Farm)
admin.site.register(Crop)
admin.site.register(Production)

