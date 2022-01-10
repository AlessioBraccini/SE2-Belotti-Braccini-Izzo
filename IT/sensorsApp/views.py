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

'''
class HumidityData(object):
    district = None
    humidity = None
    temperature = None

    def __init__(self, district, humidity, temperature):
        self.district = district
        self.humidity = humidity
        self.temperature = temperature
'''


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

        # mylist = []
        humidity_list = []
        temperature_list = []

        for district in User.DISTRICTS:
            try:
                data = HumiditySensor.objects.get(district=district[0])
                humidity_list.append(data.humidity)
                temperature_list.append(data.temperature)
                # obj = HumidityData(district[0], data.humidity, data.temperature)
                # mylist.append(obj)
            except HumiditySensor.DoesNotExist:
                # obj = HumidityData(district[0], 0, 0)
                # mylist.append(obj)
                humidity_list.append(20)
                temperature_list.append(50)
            except HumiditySensor.MultipleObjectsReturned:
                data = HumiditySensor.objects.filter(district=district[0])
                humidity_list.append(data[0].humidity)
                temperature_list.append(data[0].temperature)

        context = {
            'humidity': humidity_list,
            'temperature': temperature_list,
        }

        data = json.dumps(context)
        # json_string = json.dumps([el.__dict__ for el in mylist])
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
                water_qty_list.append(50)
            except WaterIrrigationSensor.MultipleObjectsReturned:
                data = HumiditySensor.objects.filter(district=district[0])
                water_qty_list.append(data[0].water_qty)

        context = {
            'water_qty': water_qty_list,
        }

        data = json.dumps(context)
        return HttpResponse(data)
