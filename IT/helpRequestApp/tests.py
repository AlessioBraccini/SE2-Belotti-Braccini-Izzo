from django.test import TestCase
from django.contrib.auth import get_user_model
from helpRequestApp.models import HelpRequest
from rest_framework.authtoken.models import Token
from django.test import Client
from datetime import datetime
import json

User = get_user_model()


# Create your tests here.


# Test case for the class HelpRequest
class TestHelpRequests(TestCase):
    # Set up the database and log in two users
    def setUp(self):
        self.user = User.objects.create(email="shaleenakumari@gmail.com", first_name="Shaleena", last_name="Kumari",
                                        job_role="A",
                                        district="Medak", password="userpwd")

        self.pm = User.objects.create(email="pajeetsharma@gmail.com", first_name="Pajeet", last_name="Sharma",
                                      job_role="P",
                                      district="Adilabad", password="policymakerpwd")

        self.farmer1 = User.objects.create(email="apupatel@gmail.com", first_name="Apu", last_name="Patel",
                                           job_role="F",
                                           district="Medak", password="farmer1pwd")

        self.farmer2 = User.objects.create(email="chandranprasad@gmail.com", first_name="Chandran", last_name="Prasad",
                                      job_role="F",
                                      district="Medak", password="farmer2pwd")

        self.help_request = HelpRequest.objects.create(date="2021/12/12", subject="First Subject",
                                                       message="First Message", receiver_id=self.user.id,
                                                       sender_id=self.farmer1.id)

        HelpRequest.objects.create(date="2021/08/21", subject="Second Subject",
                                   message="Second Message", receiver_id=self.user.id, sender_id=self.farmer2.id)

        user_token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + user_token.key)
        pm_token, created = Token.objects.get_or_create(user=self.pm)
        self.pm_client = Client(HTTP_AUTHORIZATION='Token ' + pm_token.key)

    # test the GET request on 'help_request' endpoint that allow a user to get the list of help requests which still needs to be answered
    def test_get_help_request(self):
        response = self.client.get('http://localhost:8000/api/v1/help_request')
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)

        self.assertEqual(json_response[0]['sender_name'], "Apu Patel")
        self.assertEqual(json_response[0]['date'], datetime.today().strftime('%Y/%m/%d'))
        self.assertEqual(json_response[0]['subject'], "First Subject")
        self.assertEqual(json_response[0]['message'], "First Message")

        self.assertEqual(json_response[1]['sender_name'], "Chandran Prasad")
        self.assertEqual(json_response[1]['date'], datetime.today().strftime('%Y/%m/%d'))
        self.assertEqual(json_response[1]['subject'], "Second Subject")
        self.assertEqual(json_response[1]['message'], "Second Message")

        # there are two help requests that need to be answered
        self.assertEqual(len(json_response), 2)

    # test the GET request on 'help_request' endpoint in case of an invalid user, verify the correct generation of the 404 error
    def test_invalid_get_help_request(self):
        response = self.pm_client.get('http://localhost:8000/api/v1/help_request')
        self.assertEqual(response.status_code, 404)

    # test the POST request on 'help_request' endpoint that allow the user to reply to an existing help request
    def test_post_help_request(self):
        payload = {
            'reply': 'Reply Message',
            'request_id': self.help_request.id,
        }

        response = self.client.post('http://localhost:8000/api/v1/help_request', data=payload)
        self.assertEqual(response.status_code, 200)

        help_request = HelpRequest.objects.get(message="Reply Message")
        # verify that the old request has been deleted
        self.assertFalse(HelpRequest.objects.filter(message="First Message").exists())
        # verify that the new request has been successfully saved
        self.assertTrue(HelpRequest.objects.filter(message="Reply Message").exists())
        # verify that the subject of the help request remained unchanged
        self.assertEqual(help_request.subject, "First Subject")
        # verify that the receiver now is the original sender
        self.assertEqual(help_request.receiver_id, self.farmer1.id)
        # verify that the sender now is the original receiver, the one who answered
        self.assertEqual(help_request.sender_id, self.user.id)

    # test the POST request on 'help_request' endpoint in case of an invalid request_id, verify the correct generation of the 404 error
    def test_invalid_post_help_request(self):
        payload = {
            'reply': 'Reply Message',
            'request_id': 10,
        }

        response = self.client.post('http://localhost:8000/api/v1/help_request', data=payload)
        self.assertEqual(response.status_code, 404)


# Test case for the class HelpRequestByID
class TestHelpRequestsByID(TestCase):
    # Set up the database and log in the user
    def setUp(self):
        self.user = User.objects.create(email="shaleenakumari@gmail.com", first_name="Shaleena", last_name="Kumari",
                                        job_role="A",
                                        district="Medak", password="userpwd")

        self.farmer = User.objects.create(email="apupatel@gmail.com", first_name="Apu", last_name="Patel",
                                          job_role="F",
                                          district="Medak", password="farmer1pwd")

        self.help_request = HelpRequest.objects.create(date="2021/12/12", subject="First Subject",
                                                       message="First Message", receiver_id=self.user.id,
                                                       sender_id=self.farmer.id)

        user_token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + user_token.key)

    # test the GET request on 'help_request_by_id' endpoint that allow the user to get a help request by ID
    def test_get_help_request_by_id(self):
        response = self.client.get('http://localhost:8000/api/v1/help_request_by_id',
                                   {'request_id': self.help_request.id})
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.content)
        self.assertEqual(json_response['sender_name'], "Apu Patel")
        self.assertEqual(json_response['date'], datetime.today().strftime('%Y/%m/%d'))
        self.assertEqual(json_response['subject'], "First Subject")
        self.assertEqual(json_response['message'], "First Message")

    # test the GET request on 'help_request_by_id' endpoint in case of an invalid user, verify the correct generation of the 404 error
    def test_invalid_get_help_request_by_id(self):
        response = self.client.get('http://localhost:8000/api/v1/help_request_by_id', {'request_id': 50})
        self.assertEqual(response.status_code, 404)
