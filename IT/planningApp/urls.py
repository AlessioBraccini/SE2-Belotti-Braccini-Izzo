from django.urls import path

from . import views

app_name = 'PlanningApp'
urlpatterns = [
    path('daily_plan', views.DailyPlanView.as_view(), name='daily_plan'),
]