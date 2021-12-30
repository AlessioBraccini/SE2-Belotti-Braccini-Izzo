from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from app.models import Farm
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
