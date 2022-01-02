from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from .models import *
from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

User = get_user_model()


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

# Create your views here.


class SteeringInitiativeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        agro = User.objects.get(id=request.user.id)


class DownloadReport(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def get(request):
        pm = User.objects.get(id=request.user.id)
        # todo: check if pm is a pm, if is agro then allow download just for own reports
        author_id = request.data['author_id']
        agro = User.objects.get(id=author_id)
        pub_date = request.data['pub_date']
        file_name = request.data['file_name']
        report = SteeringInitiative.objects.get(author=agro, pub_date=pub_date).report

        # get an open file handler:
        file_handle = report.file.open()

        # send file
        response = FileResponse(file_handle, content_type='pdf')
        response['Content-Length'] = report.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % report.file.name

        return response

