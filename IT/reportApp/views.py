import json

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
        if agro.job_role == "A":
            report = SteeringInitiative(author=agro, title=request.data['title'], report=request.FILES['file'])
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        report.save()
        return Response()

    @staticmethod
    def get(request):
        user = User.objects.get(id=request.user.id)
        if user.job_role == "P":
            reports = SteeringInitiative.objects.all()
        elif user.job_role == "A":
            reports = SteeringInitiative.objects.filter(author=user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = []
        for report in reports:
            data.append({
                'author_id': report.author.id,
                'author': report.author.complete_name(),
                'pub_date': report.pub_date,
                'file_name': report.title,
            })

        formatted_data = {'reports_list': data}

        return Response(formatted_data)


class DownloadReport(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def get(request):
        user = User.objects.get(id=request.user.id)
        author_id = request.GET.get('author_id')
        agro = User.objects.get(id=author_id)
        if user.job_role == "P" or (user.job_role == "A" and agro == user):
            pub_date = request.GET.get('pub_date')
            file_name = request.GET.get('file_name')
            try:
                report = SteeringInitiative.objects.get(author=agro, pub_date=pub_date, title=file_name).report
            except SteeringInitiative.DoesNotExist:
                return Response({"message": "No report entry for this date, file_name and agronomist"}, status=status.HTTP_404_NOT_FOUND)

            # get an open file handler:
            try:
                file_handle = report.open()
            except FileNotFoundError:
                return Response({"message": "No file found"}, status=status.HTTP_404_NOT_FOUND)

            # send file
            response = FileResponse(file_handle, content_type='pdf')
            response['Content-Length'] = report.file.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % report.file.name
        else:
            response = Response(status=status.HTTP_403_FORBIDDEN)

        return response

