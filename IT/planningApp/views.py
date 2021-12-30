from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
# from .serializers import *
from .models import *
import json

User = get_user_model()

# Create your views here.
# DONE create a new daily plan -> date, list of farms
# return list of farms to choose from -> farm and last visit/counter
# modify existing daily plan -> add and remove farm
# DONE return daily plan
# add annotations


class DailyPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        agro = User.objects.get(id=request.user.id)
        farmers_ids = request.data['visit_farmers_list']
        farmers_ids = list(farmers_ids.split(","))
        date = request.data['date']
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
            plan.save()
        return Response({"message:" "New daily plan saved successfully."})

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

