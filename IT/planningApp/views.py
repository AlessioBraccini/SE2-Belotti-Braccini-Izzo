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
        agro = User.objects.get(id=request.user.id)
        farmers_list = []
        try:
            plans = DailyPlan.objects.filter(agronomist_user__id=agro.id, date=request.data['date'])
        except DailyPlan.DoesNotExist:
            return Response({"message": "daily plan not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for plan in plans:
            farmers_list.append((plan.visit_farmer.id, plan.annotation))

        response_payload = {
            'date': request.data['date'],
            'visit_farmers_list': farmers_list,
        }
        return Response(response_payload)


class UpdateVisits(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        agro = User.objects.get(id=request.user.id)
        try:
            farmer = User.objects.get(id=request.data['visit_farmer'])
        except User.DoesNotExist:
            return Response({"message": "Farmer not found"}, status=status.HTTP_404_NOT_FOUND)
        date = request.data["date"]
        '''
        try:
            annotation = request.data["annotation"]
        except MultiValueDictKeyError:
            annotation = None
        '''
        if date < datetime.date.today():
            return Response({"message": "Cannot modify already confirmed plans"}, status=status.HTTP_403_FORBIDDEN)

        # either add, delete, add_annotation
        action = request.GET.get('action')

        if action == 'add':
            plan_entry = DailyPlan(agronomist_user=agro, date=date, visit_farmer=farmer)
            farm = Farm.objects.get(user=plan_entry.visit_farmer)
            farm.visit_ctr += 1
            farm.save()  # update visit counter farm
            plan_entry.save()
            return Response({"message": "New visit registered successfully"})
        '''
        if action == 'add_annotation':
            if annotation is not None:
                plan_entry = DailyPlan.objects.get(agronomist_user=agro, date=date, visit_farmer=farmer)
                plan_entry.annotation = annotation
                plan_entry.save()
            return Response({"message": "Daily plan entry updated successfully"})
        '''
        if action == 'delete':
            plan_entry = DailyPlan.objects.get(agronomist_user=agro, date=date, visit_farmer=farmer)
            farm = Farm.objects.get(user=plan_entry.visit_farmer)
            farm.visit_ctr -= 1
            farm.save()  # update visit counter farm
            DailyPlan.delete(plan_entry)
            return Response({"message": "Visit deleted successfully"})
        return Response({"message": "Action is not a valid one. Choose between add, add_annotation or delete"},
                            status=status.HTTP_400_BAD_REQUEST)
