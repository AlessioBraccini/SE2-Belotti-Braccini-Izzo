from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # gets custom user from settings AUTH_USER_MODEL


# Create your models here.

class HelpRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver', null=True)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
