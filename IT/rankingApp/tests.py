from django.test import TestCase
from django.contrib.auth import get_user_model
from app.models import Farm, Crop
from rest_framework.authtoken.models import Token
from django.test import Client
import json

User = get_user_model()

# Create your tests here.


# Test case for the class RankFarmers
class TestRankFarmers(TestCase):
    # Set up the database and log in two users
    def setUp(self):
        # create an agronomist
        self.agronomist = User.objects.create(email="shaleenakumari@gmail.com", first_name="Shaleena",
                                              last_name="Kumari",
                                              job_role="A",
                                              district="Medak", password="agronomistpwd")

        # create a policymaker
        self.policymaker = User.objects.create(email="pajeetsharma@gmail.com", first_name="Pajeet", last_name="Sharma",
                                               job_role="P",
                                               district="Adilabad", password="policymakerpwd")

        # create the first farmer
        self.farmer1 = User.objects.create(email="apupatel@gmail.com", first_name="Apu", last_name="Patel",
                                           job_role="F",
                                           district="Medak", password="farmer1pwd")
        farm1 = Farm.objects.create(user=self.farmer1, address="P. G. Road, Ibsl, Ground Floor, Krishna Castle", score=5881, visit_ctr=0)
        Crop.objects.create(farm=farm1, crop_type=["Wheat", "Rice"])

        # create the second farmer
        self.farmer2 = User.objects.create(email="chandranprasad@gmail.com", first_name="Chandran", last_name="Prasad",
                                           job_role="F",
                                           district="Medak", password="farmer2pwd")
        farm2 = Farm.objects.create(user=self.farmer2, address="Plot No.37, Survey No.45, Kondapur Main Road, Kondapur", score=2526, visit_ctr=2)
        Crop.objects.create(farm=farm2, crop_type=["Mais"])

        # create the third farmer
        self.farmer3 = User.objects.create(email="damayantiram@gmail.com", first_name="Damayanti",
                                           last_name="Ram",
                                           job_role="F",
                                           district="Adilabad", password="farmer3pwd")
        farm3 = Farm.objects.create(user=self.farmer3, address="Kphb Colony Phase 3, Kukatpally, Kukatpally Housing Board", score=822, visit_ctr=1)
        Crop.objects.create(farm=farm3, crop_type=["Rice"])

        # log in two users and retrieve the token in order to do get/post requests as an authenticated user
        agro_token, created = Token.objects.get_or_create(user=self.agronomist)
        self.agro_client = Client(HTTP_AUTHORIZATION='Token ' + agro_token.key)
        pm_token, created = Token.objects.get_or_create(user=self.policymaker)
        self.pm_client = Client(HTTP_AUTHORIZATION='Token ' + pm_token.key)

    # test agronomist get_ranking call with descending order specified
    def test_agronomist_get_ranking_descending(self):
        response = self.agro_client.get('/api/v1/rank_farmers', {'ordering': 'descending'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Apu Patel")
        self.assertEqual(json_response[0]['score'], 5881)
        self.assertEqual(json_response[1]['name'], "Chandran Prasad")
        self.assertEqual(json_response[1]['score'], 2526)
        # there are only two farmers with the same district of the agronomist
        self.assertEqual(len(json_response), 2)

    # test agronomist get_ranking call with ascending order specified
    def test_agronomist_get_ranking_ascending(self):
        response = self.agro_client.get('/api/v1/rank_farmers', {'ordering': 'ascending'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Chandran Prasad")
        self.assertEqual(json_response[0]['score'], 2526)
        self.assertEqual(json_response[1]['name'], "Apu Patel")
        self.assertEqual(json_response[1]['score'], 5881)
        # there are only two farmers with the same district of the agronomist
        self.assertEqual(len(json_response), 2)

    # test policymaker get_ranking call with descending order and district among the parameters of the GET request
    def test_policymaker_get_ranking_descending_with_district(self):
        response = self.pm_client.get('/api/v1/rank_farmers', {'ordering': 'descending', 'district': 'Medak'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Apu Patel")
        self.assertEqual(json_response[0]['score'], 5881)
        # there are two farmers with the district specified by the policymaker
        self.assertEqual(len(json_response), 2)

    # test policymaker get_ranking call with ascending order and district among the parameters of the GET request
    def test_policymaker_get_ranking_ascending_with_district(self):
        response = self.pm_client.get('/api/v1/rank_farmers', {'ordering': 'ascending', 'district': 'Medak'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Chandran Prasad")
        self.assertEqual(json_response[0]['score'], 2526)
        # there are two farmers with the district specified by the policymaker
        self.assertEqual(len(json_response), 2)

    # test policymaker get_ranking call with a different district
    def test_policymaker_get_ranking_with_different_district(self):
        response = self.pm_client.get('/api/v1/rank_farmers', {'ordering': 'ascending', 'district': 'Adilabad'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Damayanti Ram")
        self.assertEqual(json_response[0]['score'], 822)
        # there is only one farmer with the district specified by the policymaker
        self.assertEqual(len(json_response), 1)

    # test policymaker get_ranking call with descending order but without the district among the parameters of the GET request
    def test_policymaker_get_ranking_descending_without_district(self):
        response = self.pm_client.get('/api/v1/rank_farmers', {'ordering': 'descending'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Apu Patel")
        self.assertEqual(json_response[0]['score'], 5881)
        self.assertEqual(json_response[1]['name'], "Chandran Prasad")
        self.assertEqual(json_response[1]['score'], 2526)
        self.assertEqual(json_response[2]['name'], "Damayanti Ram")
        self.assertEqual(json_response[2]['score'], 822)
        # there are three farmers registered to the application
        self.assertEqual(len(json_response), 3)

    # test policymaker get_ranking call with ascending order but without the district among the parameters of the GET request
    def test_policymaker_get_ranking_ascending_without_district(self):
        response = self.pm_client.get('/api/v1/rank_farmers', {'ordering': 'ascending'})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['name'], "Damayanti Ram")
        self.assertEqual(json_response[0]['score'], 822)
        self.assertEqual(json_response[1]['name'], "Chandran Prasad")
        self.assertEqual(json_response[1]['score'], 2526)
        self.assertEqual(json_response[2]['name'], "Apu Patel")
        self.assertEqual(json_response[2]['score'], 5881)
        # there are three farmers registered to the application
        self.assertEqual(len(json_response), 3)


# Test case for the class ProfileFarmers
class TestProfileFarmers(TestCase):
    # Set up the database and log in the user
    def setUp(self):
        self.user = User.objects.create(email="shaleenakumari@gmail.com", first_name="Shaleena", last_name="Kumari",
                                        job_role="A",
                                        district="Medak", password="userpwd")

        farmer = User.objects.create(email="apupatel@gmail.com", first_name="Apu", last_name="Patel",
                                     job_role="F",
                                     district="Medak", password="farmer1pwd")
        farm = Farm.objects.create(user=farmer, address="M. G Road, Opposite Gopal Swamy Temple", score=5881, visit_ctr=0)
        self.farm_id = farm.id
        Crop.objects.create(farm=farm, crop_type=["Wheat", "Rice"])

        user_token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # test the GET request on 'profile_info' endpoint that allow the user to get all the info about a farmer
    def test_get_farmer_profile(self):
        response = self.client.get('/api/v1/profile_info', {'ordering': 'descending', 'farmer_id': self.farm_id})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['full_name'], "Apu Patel")
        self.assertEqual(json_response['email'], "apupatel@gmail.com")
        self.assertEqual(json_response['address'], "M. G Road, Opposite Gopal Swamy Temple")
        self.assertEqual(json_response['area'], "Medak")
        self.assertEqual(json_response['score'], 5881)
        self.assertEqual(json_response['crop_types'][0]['crop_type'], "['Wheat', 'Rice']")

    # test the GET request on 'profile_info' endpoint in case of an invalid user, verify the correct generation of the 404 error
    def test_get_farmer_profile_error(self):
        response = self.client.get('/api/v1/profile_info', {'ordering': 'descending', 'farmer_id': 10})
        self.assertEqual(response.status_code, 404)
