from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from sensorsApp.models import HumiditySensor, WaterIrrigationSensor
import json

User = get_user_model()

# Create your views here.


class Humidity(APIView):
    """
    View to manage the humidity sensors data.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return an array with humidity and temperature data for every district.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        humidity_list = []
        temperature_list = []

        for district in User.DISTRICTS:
            try:
                data = HumiditySensor.objects.get(district=district[0])
                humidity_list.append(data.humidity)
                temperature_list.append(data.temperature)
            except HumiditySensor.DoesNotExist:
                humidity_list.append(0)
                temperature_list.append(0)
            except HumiditySensor.MultipleObjectsReturned:
                data = HumiditySensor.objects.filter(district=district[0])
                humidity_list.append(data[0].humidity)
                temperature_list.append(data[0].temperature)

        context = {
            'humidity': humidity_list,
            'temperature': temperature_list,
        }

        data = json.dumps(context)
        return HttpResponse(data)


class WaterIrrigation(APIView):
    """
    View to manage the water irrigation sensors data.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        Return an array with water irrigation data for every district.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        water_qty_list = []

        for district in User.DISTRICTS:
            try:
                data = WaterIrrigationSensor.objects.get(district=district[0])
                water_qty_list.append(data.water_qty)
            except WaterIrrigationSensor.DoesNotExist:
                water_qty_list.append(0)
            except WaterIrrigationSensor.MultipleObjectsReturned:
                data = WaterIrrigationSensor.objects.filter(district=district[0])
                water_qty_list.append(data[0].water_qty)

        context = {
            'water_qty': water_qty_list,
        }

        data = json.dumps(context)
        return HttpResponse(data)
