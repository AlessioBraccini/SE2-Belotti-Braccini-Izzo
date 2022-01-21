from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .models import *
from django.http import FileResponse
from rest_framework import renderers
from rest_framework.decorators import action
import datetime

User = get_user_model()


class PassthroughRenderer(renderers.BaseRenderer):
    """
    Renderer for report file.
    Return data as-is. View have to supply a Response.
    """
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=media_type, renderer_context=None):
        return data


class SteeringInitiativeView(APIView):
    """
    Manage the upload of a new report about Steering Initiatives carried out by the agronomist
    user, as well as the listing of the reports submitted to the app.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        """
        Allow agronomist user to upload a new report.
        The request must include the following fields:
            - 'title': title of the report
            - 'file': actual pdf file of the report

        Mind that no duplicates are accepted (i.e. the same agronomist cannot upload more than one report with the
        same title in one day).

        Publishing date is added automatically with the current day date.

        :param request:
        :return: HTTPResponse status 200 if report file added correctly, error otherwise
        """
        agro = User.objects.get(id=request.user.id)
        if agro.job_role == "A":
            report_file = request.FILES['file']
            try:
                # check if file is present and functional
                report_file.open()
            except FileNotFoundError:
                return Response({"message": "No file found!"}, status=status.HTTP_400_BAD_REQUEST)
            # check no duplicates
            if SteeringInitiative.objects.filter(author=agro,
                                                title=request.data['title'],
                                                pub_date=datetime.date.today()).count() > 0:
                return Response({'message': 'Duplicate report found. Request failed.'},
                                status=status.HTTP_403_FORBIDDEN)
            else:
                report = SteeringInitiative(author=agro, title=request.data['title'], report=report_file)
                report.save()
                report_file.close()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response()

    @staticmethod
    def get(request):
        """
        Retrieve a list of the reports uploaded to the app.

        Mind that all the reports will be presented to policy maker users, while agronomist users will be presented
        with just the ones written by themselves.

        If the request can be fulfilled, the response will contain the list of reports ('reports_list') with the following fields for
        each object:
            - 'author_id'
            - 'author': full name of the report's author
            - 'pub_date': publishing date
            - 'file_name'

        :param request:
        :return: HTTPResponse status 200 if user is allowed to download the list of reports,
        error otherwise.
        """
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
    """
    Manage the download of report files.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def get(request):
        """
        Retrieve report file specified by the request through mandatory parameters:
            - 'author_id'
            - 'pub_date'
            - 'file_name'
        :return: HTTPResponse status 200 if the report exists in database and user has permissions, error otherwise
        """
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
            response = FileResponse(file_handle, content_type='multipart/form-data')
            response['Content-Length'] = report.file.size
            response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % report.file.name
        else:
            response = Response(status=status.HTTP_403_FORBIDDEN)

        return response

