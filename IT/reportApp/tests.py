import datetime
import json

from django.test import TestCase, Client
from app.models import Farm
from .models import SteeringInitiative
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.


class MyTest(TestCase):

    def setUp(self):
        self.userPm = User.objects.create(email="chickenSlayer@shutUp.com", first_name="Alister", last_name="Kenobi",
                                          job_role="P", district="Medak", password="svcsUvbiv8")
        self.userA = User.objects.create(email="foo@email.com", first_name="Banana", last_name="Joe", job_role="A",
                                         district="Sangareddy", password="bvFiebvbv9")

        token1, created = Token.objects.get_or_create(user=self.userA)
        self.client_agro = Client(HTTP_AUTHORIZATION='Token ' + token1.key)
        token2, created = Token.objects.get_or_create(user=self.userPm)
        self.client_pm = Client(HTTP_AUTHORIZATION='Token ' + token2.key)

    def testNewReportUpload_byAgro(self):
        url = "/api/v1/steering_initiatives"
        file = SimpleUploadedFile("/users/Ottavia/Documents/bonus.pdf", b"pdf")
        data = {
            'title': "A day in a life of an agronomist",
            'file': file
        }

        headers = {'content_type': 'multipart/form-data'}

        response = self.client_agro.post(url, data=data, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SteeringInitiative.objects.count(), 1)
        self.assertEqual(SteeringInitiative.objects.get().author, self.userA)
        self.assertEqual(SteeringInitiative.objects.get().pub_date, datetime.date.today())
        self.assertEqual(SteeringInitiative.objects.get().title, "A day in a life of an agronomist")

    def testNewReportUpload_byPm(self):
        url = "/api/v1/steering_initiatives"
        file = SimpleUploadedFile("../DD/DD.pdf", b"pdf")
        data = {
            'title': "A day in a life of a policy maker",
            'file': file
        }

        response = self.client_pm.post(url, data, content_type='multipart/form-data')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # Not an agronomist

    def testGetReports(self):
        # todo: add another report from the same agro and one from another agro

        url = "/api/v1/steering_initiatives"
        file = SimpleUploadedFile("/Users/Ottavia/Documents/bonus.pdf", b"pdf")
        headers = {'content_type': 'multipart/form-data'}
        data = {
                'title': "A day in a life of an agronomist",
                'file': file
            }
        self.client_agro.post(url, data, headers=headers)
        data = {
                'title': "A day in a life of an agronomist2",
                'file': file
            }

        self.client_agro.post(url, data, headers=headers)

        response2 = self.client_pm.get(url)

        print(response2.data)
        reports_list = response2.data['reports_list']

        for report in reports_list:
            self.assertEqual(response2.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response2.data['reports_list']), 2)
            self.assertEqual(report['author_id'], self.userA.id)
            self.assertEqual(report['author'], self.userA.complete_name())
            self.assertEqual(report['pub_date'], datetime.date.today())

    # todo: two different agro uploading same title report, agro get the reports (only his)
