# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # gets custom user from settings AUTH_USER_MODEL


class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    score = models.IntegerField()
    visit_ctr = models.IntegerField(default=0)


class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True)
    crop_type = models.CharField(max_length=100)


class Production(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=100)
    qty_sown = models.IntegerField()
    sown_date = models.DateField()
    qty_harvested = models.IntegerField()
    harvested_date = models.DateField()


class HelpRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver', null=True)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()



