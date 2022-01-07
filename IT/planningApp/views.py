import datetime

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from .models import *
from app.models import Farm
import json

User = get_user_model()

# Create your views here.
# todo: remove annotation from db and methods


class DailyPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        agro = User.objects.get(id=request.user.id)
        if agro.job_role != "A":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        farmers_ids = request.data['visit_farmers_list']
        date = request.data['date']
        if DailyPlan.objects.filter(agronomist_user=agro, date=date).count() > 0:
            return Response({"message": "This user already have a plan for this date"}, status=status.HTTP_403_FORBIDDEN)
        # todo: normalize date to be always in format YYYY-MM-DD
        daily_plans = []
        for farmer_id in farmers_ids:
            user = User.objects.get(id=farmer_id)
            if user is not None:
                daily_plan = DailyPlan(agronomist_user=agro, date=date, visit_farmer=user)
                daily_plans.append(daily_plan)
            else:
                return Response({"message": "one or more farms don't exist"}, status=status.HTTP_400_BAD_REQUEST)
        # all farmers have been found so commit to db the new entries
        for plan in daily_plans:
            farm = Farm.objects.get(user=plan.visit_farmer)
            farm.visit_ctr += 1
            farm.save()  # update visit counter farm
            plan.save()
        return Response({"message": "New daily plan saved successfully."})

    @staticmethod
    def get(request):
        """
        :param request:
        :return: list of date for which the agronomist has a daily plan
        """
        agro = User.objects.get(id=request.user.id)

        if agro.job_role != "A":
            return Response(status=status.HTTP_403_FORBIDDEN)

        plan_entries = DailyPlan.objects.filter(agronomist_user=agro).values('date').distinct()
        dates = []
        for entry in plan_entries:
            dates.append(entry)

        return Response(dates)


class UpdateVisits(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        agro = User.objects.get(id=request.user.id)
        date = request.data["date"]

        if date < str(datetime.date.today()):
            return Response({"message": "Cannot modify already confirmed plans"}, status=status.HTTP_403_FORBIDDEN)

        old_plan_entries = DailyPlan.objects.filter(agronomist_user=agro, date=date)
        for plan in old_plan_entries:
            farm = Farm.objects.get(user=plan.visit_farmer)
            farm.visit_ctr = 0 if farm.visit_ctr-1 < 0 else farm.visit_ctr-1
            farm.save()
        old_plan_entries.delete()

        # make the new insertion
        response = DailyPlanView.post(request)

        if response.data['message'] == 'New daily plan saved successfully.':
            return Response({"message": "Daily plan for date " + date + " has been updated successfully."})
        # todo: if error, reload the old_plan_entries
        return response

    @staticmethod
    def get(request):
        """
        Return a list of the farms in the current daily plan
        :param request: request that specify the date of the daily plan the user wants to know of
        :return: list of farms in the daily plan
        """
        agro = User.objects.get(id=request.user.id)
        farmers_list = []
        try:
            plans = DailyPlan.objects.filter(agronomist_user__id=agro.id, date=request.GET.get('date'))
        except DailyPlan.DoesNotExist:
            return Response({"message": "daily plan not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for plan in plans:
            context = {
                'farmer_id': plan.visit_farmer.id,
                'farmer_name': plan.visit_farmer.complete_name(),
            }
            farmers_list.append(context)

        response_payload = {
            'date': request.GET.get('date'),
            'visit_farmers_list': farmers_list,
        }
        return Response(response_payload)
