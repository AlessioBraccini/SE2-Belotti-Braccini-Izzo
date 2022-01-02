from django.urls import path

from .views import *

app_name = 'reportApp'
urlpatterns = [
    path('steering_initiatives', SteeringInitiativeView.as_view(), name='steering_initiatives'),
    path('download_reports', DownloadReport.as_view(), name='download_reports'),
    ]
