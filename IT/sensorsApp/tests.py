from django.test import TestCase
from django.contrib.auth import get_user_model
from sensorsApp.models import HumiditySensor, WaterIrrigationSensor
from rest_framework.authtoken.models import Token
from django.test import Client
import json

User = get_user_model()


# Create your tests here.

# Test case for the class Humidity
class TestHumidity(TestCase):
    # Set up the database and log in two users
    def setUp(self):
        # create a user
        self.user = User.objects.create(email="pajeetsharma@gmail.com", first_name="Pajeet", last_name="Sharma",
                                        job_role="P",
                                        district="Adilabad", password="policymakerpwd")

        HumiditySensor.objects.create(district="Medak", humidity=80, temperature=26)
        HumiditySensor.objects.create(district="Medak", humidity=82, temperature=27)
        HumiditySensor.objects.create(district="Hyderabad", humidity=78, temperature=25)

        user_token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # test the GET request on 'humidity' endpoint that allow the user to get all the humidity sensors data
    def test_get_humidity(self):
        response = self.client.get('/api/v1/humidity')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)

        # verify that there is one value for each district in Telangana
        self.assertEqual(len(json_response['humidity']), 33)
        self.assertEqual(len(json_response['temperature']), 33)

        # verify the insertion of the values
        self.assertTrue(json_response['humidity'].count(80) == 1)
        self.assertTrue(json_response['temperature'].count(26) == 1)
        self.assertTrue(json_response['humidity'].count(78) == 1)
        self.assertTrue(json_response['temperature'].count(25) == 1)
        self.assertTrue(json_response['humidity'].count(0) == 31)
        self.assertTrue(json_response['temperature'].count(0) == 31)

        # verify that for districts with multiple entries only the first one is used (Medak district case)
        self.assertTrue(json_response['humidity'].count(82) == 0)
        self.assertTrue(json_response['temperature'].count(27) == 0)


# Test case for the class WaterIrrigation
class TestWaterIrrigation(TestCase):
    # Set up the database and log in two users
    def setUp(self):
        # create a user
        self.user = User.objects.create(email="pajeetsharma@gmail.com", first_name="Pajeet", last_name="Sharma",
                                        job_role="P",
                                        district="Adilabad", password="policymakerpwd")

        WaterIrrigationSensor.objects.create(district="Hanumakonda", water_qty=112)
        WaterIrrigationSensor.objects.create(district="Hanumakonda", water_qty=88)
        WaterIrrigationSensor.objects.create(district="Nizamabad", water_qty=96)

        user_token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # test the GET request on 'water_irrigation' endpoint that allow the user to get all the water irrigation sensors data
    def test_get_water_irrigation(self):
        response = self.client.get('/api/v1/water_irrigation')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        print(json_response)

        # verify that there is one value for each district in Telangana
        self.assertEqual(len(json_response['water_qty']), 33)

        # verify the insertion of the values
        self.assertTrue(json_response['water_qty'].count(112) == 1)
        self.assertTrue(json_response['water_qty'].count(96) == 1)
        self.assertTrue(json_response['water_qty'].count(0) == 31)

        # verify that for districts with multiple entries only the first one is used (Hanumakonda district case)
        self.assertTrue(json_response['water_qty'].count(88) == 0)
