from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import get_user_model
from app.models import Farm
import json

User = get_user_model()


# Create your views here.


def get_ranking(district, flag):
    mydict = {}
    users = User.objects.filter(district).distinct()
    farms = Farm.objects.filter(district)
    for u in users:
        if farms.filter(id=u.id).exists():
            mydict[u.complete_name()] = farms.get(id=u.id).get_score()
    if flag:
        sorted_list = sorted(mydict.items(), key=lambda x: (-x[1]))  # descending order (top farmers)
    else:
        sorted_list = sorted(mydict.items(), key=lambda x: (x[1]))  # ascending order (worst farmers)

    # sorted_list = sorted_list[0:10]  # top/worst 10
    json_string = json.dumps(sorted_list)
    return json_string


def top_farmers(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.email)
        if user is None:
            raise Http404("User not found")
        district = User.objects.get(user.district)
        if district is None:
            raise Http404("District not found")

        json_string = get_ranking(district, True)
        return JsonResponse(json_string)
    return HttpResponseBadRequest("User is not authenticated")


def worst_farmers(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.email)
        if user is None:
            raise Http404("User not found")
        district = User.objects.get(user.district)
        if district is None:
            raise Http404("District not found")

        json_string = get_ranking(district, False)
        return JsonResponse(json_string)
    return HttpResponseBadRequest("User is not authenticated")
