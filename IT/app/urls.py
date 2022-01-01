from django.urls import path

from . import views

app_name = 'App'
urlpatterns = [
    path('farms_list', views.FarmView.as_view(), name='farms_list'),
]