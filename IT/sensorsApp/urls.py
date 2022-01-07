from django.urls import path

from . import views

app_name = 'sensorsApp'
urlpatterns = [
    path('humidity', views.Humidity.as_view(), name='humidity'),
    path('water_irrigation', views.WaterIrrigation.as_view(), name='water_irrigation'),
]
