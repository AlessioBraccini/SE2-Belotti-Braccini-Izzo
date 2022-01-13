from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # gets custom user from settings AUTH_USER_MODEL

# Create your models here.


class DailyPlan(models.Model):
    agronomist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agronomist_user', null=True)
    date = models.DateField()
    visit_farmer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='visit_farmer', null=True)
    annotation = models.TextField()
