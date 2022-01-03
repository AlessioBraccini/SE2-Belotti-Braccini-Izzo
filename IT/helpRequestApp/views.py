from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from helpRequestApp.models import HelpRequest
import json

User = get_user_model()


# Create your views here.

class Request(object):
    sender_name = None
    sender_id = None
    date = None
    subject = None
    message = None

    def __init__(self, sender_name, sender_id, date, subject, message):
        self.sender_name = sender_name
        self.sender_id = sender_id
        self.date = date
        self.subject = subject
        self.message = message


class HelpRequests(APIView):
    """
    View to list the help requests.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return a list of help requests.
        """
        user = User.objects.get(email=request.user.email)
        if user is None:
            raise Http404("User not found")

        requests = []
        help_requests = HelpRequest.objects.filter(receiver_id=user.id)
        for h_request in help_requests:
            user = User.objects.get(id=h_request.sender_id)
            date = h_request.date.strftime("%Y/%m/%d")
            request = Request(user.complete_name(), h_request.sender_id, date, h_request.subject, h_request.message)
            requests.append(request)

        json_string = json.dumps([el.__dict__ for el in requests], default=str)
        return HttpResponse(json_string)
