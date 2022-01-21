from django.db import models
from django.contrib.auth import get_user_model
from gdstorage.storage import GoogleDriveStorage

User = get_user_model()

# Google Drive Storage to save static files (reports)
# gd_storage = GoogleDriveStorage()


class SteeringInitiative(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50, null=True)
    report = models.FileField(upload_to='reports/')
