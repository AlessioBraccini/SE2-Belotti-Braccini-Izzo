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
    name = None
    score = None

    def __init__(self, name, score):
        self.name = name
        self.score = score


def get_ranking(district, ordering):
    mylist = []
    if ordering == 'descending':
        farms = Farm.objects.filter(user_id__district=district).order_by('-score')
    else:
        farms = Farm.objects.filter(user_id__district=district).order_by('score')
    if farms.count() > 0:
        for f in farms:
            rank = Ranking(f.user_id.complete_name(), f.score)
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
        mylist = get_ranking(user.district, ordering)
        json_string = json.dumps(mylist, default=lambda x: x.__dict__)
        return JsonResponse(json_string, safe=False)
