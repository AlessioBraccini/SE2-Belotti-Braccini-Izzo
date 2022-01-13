from django.urls import path

from . import views

app_name = 'rankingApp'
urlpatterns = [
    path('rank_farmers', views.RankFarmers.as_view(), name='rank_farmers'),
    path('profile_info', views.ProfileFarmers.as_view(), name='profile_info'),
]
