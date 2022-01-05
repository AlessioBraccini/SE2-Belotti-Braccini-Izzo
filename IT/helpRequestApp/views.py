from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from helpRequestApp.models import HelpRequest
from datetime import datetime
import json

User = get_user_model()


# Create your views here.

class Request(object):
    request_id = None
    sender_name = None
    sender_id = None
    date = None
    subject = None
    message = None

    def __init__(self, request_id, sender_name, sender_id, date, subject, message):
        self.request_id = request_id
        self.sender_name = sender_name
        self.sender_id = sender_id
        self.date = date
        self.subject = subject
        self.message = message


class HelpRequests(APIView):
    """
    View to manage the help requests.

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
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        requests = []
        help_requests = HelpRequest.objects.filter(receiver_id=user.id)
        if not help_requests.exists():
            return Response({"message": "Help requests not found"}, status=status.HTTP_404_NOT_FOUND)
        for h_request in help_requests:
            user = User.objects.get(id=h_request.sender_id)
            if user is not None:
                date = h_request.date.strftime("%Y/%m/%d")
                request = Request(h_request.id, user.complete_name(), h_request.sender_id, date, h_request.subject, h_request.message)
                requests.append(request)

        json_string = json.dumps([el.__dict__ for el in requests], default=str)
        return HttpResponse(json_string)

    @staticmethod
    def post(request):
        """
        Save the reply to a help request.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            reply_msg = request.data['reply']
        except KeyError:
            return Response({"message": "Reply message not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            farmer_id = request.data['farmer_id']
        except KeyError:
            return Response({"message": "Sender id not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            request_id = request.data['request_id']
            help_request = HelpRequest.objects.get(id=request_id)
        except (KeyError, HelpRequest.DoesNotExist) as e:
            return Response({"message": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        subject_msg = help_request.subject
        help_request.delete()

        HelpRequest.objects.create(date=datetime.now(), subject=subject_msg, message=reply_msg, receiver_id=farmer_id, sender_id=user.id)

        return Response({"Help request reply saved successfully."})
