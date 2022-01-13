import datetime

from django.test import TestCase
from app.models import Farm
from .models import SteeringInitiative
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.


class MyTest(APITestCase):
    userF1, userF2, userF3 = None, None, None
    userPm, userA = None, None
    farm1, farm2, farm3 = None, None, None

    @classmethod
    def setUpTestData(cls):
        cls.userPm = User.objects.create_user(email="chickenSlayer@shutUp.com", first_name="Alister",
                                              last_name="Kenobi",
                                              job_role="P", district="Medak", password="svcsUvbiv8")
        cls.userA = User.objects.create_user(email="foo@email.com", first_name="Banana", last_name="Joe", job_role="A",
                                             district="Sangareddy", password="bvFiebvbv9")
        cls.userF1 = User.objects.create(email="karun@itsme.com", first_name="Karun", last_name="Patel", job_role="F",
                                         district="Sangareddy", password="fwiwbfbfi65")
        cls.userF2 = User.objects.create(email="karun@itsnotme.com", first_name="FakeKarun", last_name="Patel",
                                         job_role="F",
                                         district="Rangareddy", password="fwiwbfbfi65")
        cls.userF3 = User.objects.create(email="mario.rossi@basic.guy.com", first_name="Mario", last_name="Rossi",
                                         job_role="F",
                                         district="Sangareddy", password="fwiwbfbfi65")
        cls.farm1 = Farm.objects.create(user=cls.userF1, address="Boh Street, 12")
        cls.farm2 = Farm.objects.create(user=cls.userF2, address="Boh Street, 13")
        cls.farm3 = Farm.objects.create(user=cls.userF3, address="Boh Street, 13")

    def testNewReportUpload1(self):
        # factory = APIRequestFactory()
        client = APIClient()
        userB = User.objects.create_user(email="foo2@email.com", first_name="Banana", last_name="Joe", job_role="A",
                                         district="Sangareddy", password="bvFiebvbv9")
        token, created = Token.objects.get_or_create(user=userB)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = "/api/v1/steering_initiatives"
        # request = factory.get(url)
        # client.force_authenticate()

        data = {
            'title': "A day in a life of an agronomist",
            'file': open("/Users/Ottavia/Documents/bonus.pdf")
        }

        response = self.client.post(url, data, content_type='multipart/form-data')
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SteeringInitiative.objects.count(), 1)
        self.assertEqual(SteeringInitiative.objects.get().author, self.__class__.userA)
        self.assertEqual(SteeringInitiative.objects.get().date, datetime.date.today())
        self.assertEqual(SteeringInitiative.objects.get().title, "A day in a life of an agronomist")

        client.credentials()  # cleaning credentials

    def testNewReportUpload2(self):
        client = APIClient()
        client.force_authenticate(user=self.__class__.userPm)

        url = "/api/v1/steering_initiatives"
        data = {
            'title': "A day in a life of a policy maker",
            'file': open("../DD/DD.pdf")
        }

        response = self.client.post(url, data, content_type='multipart/form-data')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # Not an agronomist

    def testGetReports(self):
        client1 = APIClient()
        client2 = APIClient()
        # todo: add another report from the same agro and one from another agro
        client1.force_authenticate(user=self.__class__.userA)

        url = "/api/v1/steering_initiatives"
        data = {
            'title': "A day in a life of an agronomist2",
            'file': open("/Users/Ottavia/Documents/bonus.pdf")
        }
        client1.force_authenticate(None)
        client2.force_authenticate(user=self.__class__.userPm)

        self.client.post(url, data, content_type='multipart/form-data')

        response2 = self.client.get(url)

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data['author_id'], self.__class__.userA.id)
        self.assertEqual(response2.data['author'], self.__class__.userA.complete_name())
        self.assertEqual(response2.data['pub_date'], datetime.date.today())
        self.assertEqual(response2.data['file_name'], "A day in a life of an agronomist2")
