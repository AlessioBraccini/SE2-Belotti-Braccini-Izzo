import datetime, json
from django.test import TestCase, Client
from userApp.models import User
from app.models import Farm
from rest_framework.authtoken.models import Token
from .models import DailyPlan
from rest_framework import status


# Create your tests here.
# check double entries of farms
# check post only for agro
# check only existing farmers allowed
# check creation of old plans


class DailyPlanTest(TestCase):
    url = "/api/v1/daily_plan"
    url_update = "/api/v1/update_daily_plan"

    def setUp(self):
        self.userPm = User.objects.create(email="chickenSlayer@shutUp.com", first_name="Alister", last_name="Kenobi",
                                         job_role="P", district="Medak", password="svcsUvbiv8")
        self.userA = User.objects.create(email="foo@email.com", first_name="Banana", last_name="Joe", job_role="A",
                                        district="Sangareddy", password="bvFiebvbv9")

        self.userF1 = User.objects.create(email="karun@itsme.com", first_name="Karun", last_name="Patel", job_role="F",
                                        district="Sangareddy", password="fwiwbfbfi65")
        self.userF2 = User.objects.create(email="karun@itsnotme.com", first_name="FakeKarun", last_name="Patel", job_role="F",
                                        district="Rangareddy", password="fwiwbfbfi65")
        self.userF3 = User.objects.create(email="mario.rossi@basic.guy.com", first_name="Mario", last_name="Rossi", job_role="F",
                                        district="Sangareddy", password="fwiwbfbfi65")
        self.farm1 = Farm.objects.create(user=self.userF1, address="Boh Street, 12")
        self.farm2 = Farm.objects.create(user=self.userF2, address="Boh Street, 13")
        self.farm3 = Farm.objects.create(user=self.userF3, address="Boh Street, 13")

        token, created = Token.objects.get_or_create(user=self.userA)
        self.client_agro = Client(HTTP_AUTHORIZATION='Token ' + token.key)


    def testUploadNewPlan(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id],
        }

        response = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        # checks
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.all().count(), 2)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 1)

    def testUploadNewPlanNotValidRegion(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF2.id]  # F2's region doesn't match with agro
        }

        response = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.all().count(), 0)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 0)
        self.assertEqual(Farm.objects.get(user=self.userF2).visit_ctr, 0)

    def testUploadNewPlanNotValidDate(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id]
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        data = {
            'date': datetime.date.today(),  # same date as previous daily plan
            'visit_farmers_list': [self.userF3.id]
        }

        response2 = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.all().count(), 1)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 0)

    def testUploadNewPlanDuplicatedFarmer(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id, self.userF1.id]
        }

        response = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.count(), 2)
        # just one visit, post method eliminates duplicate
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 1)

    def testUploadNewPlanNotAgro(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id],
        }

        token, created = Token.objects.get_or_create(user=self.userPm)
        client_pm = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client_pm.post(self.__class__.url, data, content_type='application/json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.count(), 0)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 0)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 0)

    def testRetrievePlans(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id],
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        data = {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'visit_farmers_list': [self.userF1.id, self.userF3.id],
        }

        response2 = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 2)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 2)
        self.assertEqual(Farm.objects.get(user=self.userF2).visit_ctr, 0)

        response3 = self.client_agro.get(self.__class__.url)
        json_response = json.loads(response3.content)

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response[0]['date'], str(datetime.date.today()))
        self.assertEqual(json_response[1]['date'], str(datetime.date.today() + datetime.timedelta(days=1)))

    def testRetrieveOnlyMyPlans(self):
        agro2 = User.objects.create(email="itsame@maar.io", first_name="Mario", last_name="Blu", job_role="A",
                                        district="Sangareddy", password="fwiwbfbfi65")
        agro3 = User.objects.create(email="itsnotame@maar.io", first_name="Mario", last_name="Verdi", job_role="A",
                                        district="Rangareddy", password="fwiwbfbfi65")

        token, created = Token.objects.get_or_create(user=agro2)
        client_agro2 = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        token, created = Token.objects.get_or_create(user=agro3)
        client_agro3 = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id]
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')
        response2 = client_agro2.post(self.__class__.url, data, content_type='application/json')
        data = {
            'date': datetime.date.today() + datetime.timedelta(days=5),
            'visit_farmers_list': [self.userF1.id]
        }
        response2_bis = client_agro2.post(self.__class__.url, data, content_type='application/json')

        data = {
            'date': datetime.date.today() + datetime.timedelta(days=1),
            'visit_farmers_list': [self.userF2.id]
        }

        response3 = client_agro3.post(self.__class__.url, data, content_type='application/json')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response2_bis.status_code, status.HTTP_200_OK)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 3)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 2)
        self.assertEqual(Farm.objects.get(user=self.userF2).visit_ctr, 1)

        get1 = self.client_agro.get(self.__class__.url)
        get2 = client_agro2.get(self.__class__.url)
        get3 = client_agro3.get(self.__class__.url)

        json1 = json.loads(get1.content)
        json2 = json.loads(get2.content)
        json3 = json.loads(get3.content)

        self.assertEqual(get1.status_code, status.HTTP_200_OK)
        self.assertEqual(get2.status_code, status.HTTP_200_OK)
        self.assertEqual(get3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json1), 1)
        self.assertEqual(len(json2), 2)
        self.assertEqual(len(json3), 1)
        self.assertEqual(json1[0]['date'], str(datetime.date.today()))
        self.assertTrue(json2[0]['date'] == str(datetime.date.today())
                        or json2[0]['date'] == str(datetime.date.today() + datetime.timedelta(days=5)))
        self.assertTrue(json2[1]['date'] == str(datetime.date.today())
                        or json2[1]['date'] == str(datetime.date.today() + datetime.timedelta(days=5)))
        self.assertNotEqual(json2[0]['date'], json2[1]['date'])
        self.assertEqual(json3[0]['date'], str(datetime.date.today() + datetime.timedelta(days=1)))

    def testUpdatePlan(self):
        userF4 = User.objects.create(email="mario.rossi2@basic.guy.com", first_name="Mario2", last_name="Rossi2", job_role="F",
                                        district="Sangareddy", password="fwiwbfbfi65")
        farm4 = Farm.objects.create(user=userF4, address="Boh Street, 12")
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id, self.userF3.id]
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 1)

        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF3.id, userF4.id]
        }

        response2 = self.client_agro.post(self.__class__.url_update, data, content_type='application/json')

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 0)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=userF4).visit_ctr, 1)

        get = self.client_agro.get(self.__class__.url_update, {'date': str(datetime.date.today())})
        json_resp = json.loads(get.content)

        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_resp), 2)
        self.assertEqual(json_resp['date'], str(datetime.date.today()))
        self.assertEqual(len(json_resp['visit_farmers_list']), 2)
        self.assertTrue(json_resp['visit_farmers_list'][0]['farmer_id'] == self.userF3.id
                        or json_resp['visit_farmers_list'][0]['farmer_id'] == userF4.id)
        self.assertTrue(json_resp['visit_farmers_list'][1]['farmer_id'] == self.userF3.id
                        or json_resp['visit_farmers_list'][1]['farmer_id'] == userF4.id)

    def testUpdateOldPlan(self):
        data = {
            'date': datetime.date.today() + datetime.timedelta(days=-1),
            'visit_farmers_list': [self.userF1.id, self.userF3.id]
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        data = {
            'date': datetime.date.today() + datetime.timedelta(days=-1),
            'visit_farmers_list': [self.userF3.id]
        }

        response2 = self.client_agro.post(self.__class__.url_update, data, content_type='application/json')

        self.assertNotEqual(response2.status_code, status.HTTP_200_OK)

        get = self.client_agro.get(self.__class__.url_update,
                                   {'date': str(datetime.date.today() + datetime.timedelta(days=-1))})
        json_resp = json.loads(get.content)

        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_resp), 2)
        self.assertEqual(json_resp['date'], str(datetime.date.today() + datetime.timedelta(days=-1)))
        self.assertEqual(len(json_resp['visit_farmers_list']), 2)
        self.assertTrue(json_resp['visit_farmers_list'][0]['farmer_id'] == self.userF3.id
                        or json_resp['visit_farmers_list'][0]['farmer_id'] == self.userF1.id)
        self.assertTrue(json_resp['visit_farmers_list'][1]['farmer_id'] == self.userF3.id
                        or json_resp['visit_farmers_list'][1]['farmer_id'] == self.userF1.id)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 1)
        self.assertEqual(Farm.objects.get(user=self.userF3).visit_ctr, 1)

    def testUpdateRemovePlan(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id]
        }

        response1 = self.client_agro.post(self.__class__.url, data, content_type='application/json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': []
        }

        response2 = self.client_agro.post(self.__class__.url_update, data, content_type='application/json')

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.count(), 0)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 0)

    def testUpdateWithoutPlanEntry(self):
        data = {
            'date': datetime.date.today(),
            'visit_farmers_list': [self.userF1.id]
        }

        response = self.client_agro.post(self.__class__.url_update, data, content_type='application/json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyPlan.objects.count(), 0)
        self.assertEqual(Farm.objects.get(user=self.userF1).visit_ctr, 0)



