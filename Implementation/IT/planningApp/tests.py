from django.test import TestCase
from userApp.models import User
from app.models import Farm
from .models import DailyPlan
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.


class MyTest(TestCase):
    userF1, userF2, userF3 = None, None, None
    userPm, userA = None, None
    farm1, farm2, farm3 = None, None, None

    @classmethod
    def setUpTestData(cls):
        cls.userPm = User.objects.create(email="chickenSlayer@shutUp.com", first_name="Alister", last_name="Kenobi",
                                         job_role="P", district="Medak", password="svcsUvbiv8")
        cls.userA = User.objects.create(email="foo@email.com", first_name="Banana", last_name="Joe", job_role="A",
                                        district="Sangareddy", password="bvFiebvbv9")

        cls.userF1 = User.objects.create(email="karun@itsme.com", first_name="Karun", last_name="Patel", job_role="F",
                                        district="Sangareddy", password="fwiwbfbfi65")
        cls.userF2 = User.objects.create(email="karun@itsnotme.com", first_name="FakeKarun", last_name="Patel", job_role="F",
                                        district="Rangareddy", password="fwiwbfbfi65")
        cls.userF3 = User.objects.create(email="mario.rossi@basic.guy.com", first_name="Mario", last_name="Rossi", job_role="F",
                                        district="Sangareddy", password="fwiwbfbfi65")
        cls.farm1 = Farm.objects.create(user=cls.userF1, address="Boh Street, 12")
        cls.farm2 = Farm.objects.create(user=cls.userF2, address="Boh Street, 13")
        cls.farm3 = Farm.objects.create(user=cls.userF3, address="Boh Street, 13")

    def testNewPlan(self):
        # insert here
