from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import authentication, permissions
from .models import *

User = get_user_model()


class FarmerProfile(object):
    full_name = None
    email = None
    area = None
    visit_ctr = None
    crop_types = []

    def __init__(self, full_name, email, area, visit_ctr, crop_types):
        self.full_name = full_name
        self.email = email
        self.area = area
        self.visit_ctr = visit_ctr
        self.crop_types = crop_types

# Create your views here.


class FarmView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        agro = User.objects.get(id=request.user.id)
        if agro.job_role != 'A':
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        farms = Farm.objects.filter(user__district=agro.district).order_by('visit_ctr')

        farmers_list = []
        for farm in farms:
            context = {
                'farmer_id': farm.user.id,
                'farmer_name': farm.user.complete_name(),
                'visit_ctr': farm.visit_ctr,
            }
            farmers_list.append(context)

        return Response(farmers_list)
