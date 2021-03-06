from django.db import models
from django.contrib.auth import get_user_model
from gdstorage.storage import GoogleDriveStorage
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

User = get_user_model()

# Google Drive Storage to save static files (reports)
gd_storage = GoogleDriveStorage() if os.getenv('LOCAL_STATIC_FILES', 'true').lower() in ('false', '0', 'f') \
            else FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'generated/'),
                                   base_url=os.path.join(settings.MEDIA_URL, 'generated/'))


class SteeringInitiative(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50, null=True)
    report = models.FileField(upload_to='reports/', storage=gd_storage)
