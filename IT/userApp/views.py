from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


def account_type(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.email)
        if user is None:
            raise Http404("User not found")
        return HttpResponse(user.get_job_role())
    return HttpResponseBadRequest("User is not authenticated")

