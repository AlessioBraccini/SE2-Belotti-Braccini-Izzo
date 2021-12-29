from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # gets custom user from settings AUTH_USER_MODEL

# Create your models here.


class DailyPlan(models.Model):
    agronomist_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    farmer_user_id = models.IntegerField()
    annotation = models.TextField()
