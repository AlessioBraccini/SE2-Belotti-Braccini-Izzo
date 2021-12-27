from django.urls import path

from . import views

app_name = 'userApp'
urlpatterns = [
    path('account_type', views.account_type, name='account_type'),
]