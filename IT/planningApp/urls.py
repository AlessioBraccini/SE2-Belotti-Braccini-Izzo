from django.urls import path

from . import views

app_name = 'PlanningApp'
urlpatterns = [
    path('daily_plan', views.DailyPlanView.as_view(), name='daily_plan'),
    path('update_daily_plan', views.UpdateVisits.as_view(), name='update_daily_plan'),
]