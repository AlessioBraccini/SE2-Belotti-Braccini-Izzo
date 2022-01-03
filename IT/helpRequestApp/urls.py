from django.urls import path

from . import views

app_name = 'helpRequestApp'
urlpatterns = [
    path('help_request', views.HelpRequests.as_view(), name='help_request'),
]
