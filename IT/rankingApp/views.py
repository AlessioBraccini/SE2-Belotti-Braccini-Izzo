from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from app.models import Farm

User = get_user_model()


# Create your views here.


def get_ranking(district, ordering):
    mydict = {}
    if ordering == 'descending':
        farms = Farm.objects.filter(user_id__district=district).order_by('-score')
    else:
        farms = Farm.objects.filter(user_id__district=district).order_by('score')
    if farms.count() > 0:
        for f in farms:
            mydict[f.user_id.complete_name()] = f.score
    # sorted_list = sorted_list[0:10]  # top/worst 10
    return mydict


class RankFarmers(APIView):
    """
    View to list rank of farmers.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return a list of all users.
        """
        user = User.objects.get(email=request.user.email)
        if user is None:
            raise Http404("User not found")
        print(user.district)
        ordering = request.GET.get('ordering')
        json_string = get_ranking(user.district, ordering)
        return JsonResponse(json_string)


