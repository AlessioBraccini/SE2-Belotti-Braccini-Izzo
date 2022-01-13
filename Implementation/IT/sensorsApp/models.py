from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # gets custom user from settings AUTH_USER_MODEL


# Create your models here.


class HumiditySensor(models.Model):
    district = models.CharField(max_length=100, choices=User.DISTRICTS)
    humidity = models.IntegerField(default=0)
    temperature = models.IntegerField(default=0)


class WaterIrrigationSensor(models.Model):
    district = models.CharField(max_length=100, choices=User.DISTRICTS)
    water_qty = models.IntegerField(default=0)
