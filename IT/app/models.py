# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    JOB_ROLES = (
        ('F', 'Farmer'),
        ('A', 'Agronomist'),
        ('P', 'PolicyMaker'),
    )
    user_id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    job_role = models.CharField(max_length=1, choices=JOB_ROLES)
    district = models.CharField(max_length=100)


class Farm(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    score = models.IntegerField()


class Crop(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=100)


class Production(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=100)
    qty_sown = models.IntegerField()
    sown_date = models.DateField()
    qty_harvested = models.IntegerField()
    harvested_date = models.DateField()


class DailyPlan(models.Model):
    agronomist_user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    farmer_user_id = models.IntegerField()
    annotation = models.TextField()


class HelpRequest(models.Model):
    sender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver_id = models.IntegerField()
    subject = models.CharField(max_length=100)
    message = models.TextField()


class SteeringInitiative(models.Model):
    author_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    report = models.FileField(upload_to='files/')
