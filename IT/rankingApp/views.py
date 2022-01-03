from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from app.models import Farm, Crop
import json

User = get_user_model()


# Create your views here.

class Ranking(object):
    user_id = None
    name = None
    score = None

    def __init__(self, user_id, name, score):
        self.user_id = user_id
        self.name = name
        self.score = score


class FarmerProfile(object):
    full_name = None
    email = None
    address = None
    area = None
    score = None
    crop_types = []

    def __init__(self, full_name, email, address, area, score, crop_types):
        self.full_name = full_name
        self.email = email
        self.address = address
        self.area = area
        self.score = score
        self.crop_types = crop_types


def get_ranking(ordering, district=''):
    mylist = []

    # no district selected
    if district == '':
        if ordering == 'descending':
            farms = Farm.objects.order_by('-score')
        else:
            farms = Farm.objects.order_by('score')
    # district selected
    else:
        if ordering == 'descending':
            farms = Farm.objects.filter(user_id__district=district).order_by('-score')
        else:
            farms = Farm.objects.filter(user_id__district=district).order_by('score')

    if farms.count() > 0:
        for f in farms:
            rank = Ranking(f.id, f.user.complete_name(), f.score)
            mylist.append(rank)
    return mylist


class RankFarmers(APIView):
    """
    View to manage the ranking.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return the ranking, a list of farmers.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        ordering = request.GET.get('ordering')
        # agronomist ranking
        if user.job_role == 'A':
            mylist = get_ranking(ordering, user.district)
        # policy maker ranking
        elif user.job_role == 'P':
            # district selected
            if 'district' in request.GET:
                district = request.GET.get('district')
                mylist = get_ranking(ordering, district)
            # global ranking, district not selected
            else:
                mylist = get_ranking(ordering)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        json_string = json.dumps([el.__dict__ for el in mylist])
        return HttpResponse(json_string)


class ProfileFarmers(APIView):
    """
    View to get the profile of a farmer.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return a farmer profile.
        """
        try:
            User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        farmer_id = request.GET.get('farmer_id')
        if farmer_id is None:
            return Response({"message": "Farmer id not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            farm = Farm.objects.get(pk=farmer_id)
        except Farm.DoesNotExist:
            return Response({"message": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)

        crops = list(Crop.objects.filter(farm_id=farmer_id).values('crop_type'))
        profile_info = FarmerProfile(farm.user.complete_name(), farm.user.email, farm.address, farm.user.district, farm.score, crops)
        json_string = json.dumps(profile_info.__dict__)
        return HttpResponse(json_string)
