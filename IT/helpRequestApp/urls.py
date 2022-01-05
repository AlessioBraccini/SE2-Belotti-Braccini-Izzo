from django.urls import path

from . import views

app_name = 'helpRequestApp'
urlpatterns = [
    path('help_request', views.HelpRequests.as_view(), name='help_request'),
    path('help_request_by_id', views.HelpRequestByID.as_view(), name='help_request_by_id'),
]
