from django.urls import path

from . import views

app_name = 'rankingApp'
urlpatterns = [
    path('top_farmers', views.top_farmers, name='top_farmers'),
    path('worst_farmers', views.worst_farmers, name='worst_farmers'),
]
