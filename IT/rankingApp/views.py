from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
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
    area = None
    score = None
    crop_types = []

    def __init__(self, full_name, email, area, score, crop_types):
        self.full_name = full_name
        self.email = email
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
            rank = Ranking(f.user.id, f.user.complete_name(), f.score)
            mylist.append(rank)
    return mylist


class RankFarmers(APIView):
    """
    View to list rank of farmers.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        user = User.objects.get(email=request.user.email)
        if user is None:
            raise Http404("User not found")

        ordering = request.GET.get('ordering')
        # agronomist ranking
        if user.job_role == 'A':
            mylist = get_ranking(ordering, user.district)
        # policy maker ranking
        elif user.job_role == 'P':
            district = request.GET.get('district')
            # district selected
            if district is not None:
                mylist = get_ranking(ordering, district)
            # global ranking, district not selected
            else:
                mylist = get_ranking(ordering)

        else:
            raise Http404("User type not allowed")

        json_string = json.dumps([el.__dict__ for el in mylist])
        return HttpResponse(json_string)

        # return HttpResponse(json_string, content_type="application/json")
        # return JsonResponse(json_string, safe=False)


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
        user = User.objects.get(email=request.user.email)
        if user is None:
            raise Http404("User not found")

        farmer_id = request.GET.get('farmer_id')
        if farmer_id is None:
            raise Http404("Invalid farmer id")

        farm = Farm.objects.get(pk=farmer_id)
        user = User.objects.get(pk=farmer_id)
        crops = list(Crop.objects.filter(farm_id=farmer_id).values('crop_type'))

        profile_info = FarmerProfile(user.complete_name(), user.email, user.district, farm.score, crops)
        json_string = json.dumps(profile_info.__dict__)
        return HttpResponse(json_string)
