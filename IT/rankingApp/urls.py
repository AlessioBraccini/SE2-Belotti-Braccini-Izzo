from django.urls import path

from . import views

app_name = 'rankingApp'
urlpatterns = [
    path('rank_farmers', views.RankFarmers.as_view(), name='rank_farmers'),
]
