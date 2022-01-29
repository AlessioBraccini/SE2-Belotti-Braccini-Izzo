import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sensorsApp.models import HumiditySensor, WaterIrrigationSensor

User = get_user_model()


# Create your views here.


class Humidity(APIView):
    """
    View to manage the data requests about humidity sensors on 'humidity' endpoint.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        It handles the GET request on this endpoint, return an array with humidity and temperature values for each district.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        humidity_list = []
        temperature_list = []

        for district in User.DISTRICTS:
            try:
                data = HumiditySensor.objects.filter(district=district[0])
                count = data.count()

                if count == 0:
                    humidity_list.append(0)
                    temperature_list.append(0)
                else:
                    humidity_avg = 0
                    temperature_avg = 0
                    for n in range(count):
                        humidity_avg += data[n].humidity
                        temperature_avg += data[n].temperature
                    humidity_avg /= count
                    temperature_avg /= count
                    humidity_list.append(humidity_avg)
                    temperature_list.append(temperature_avg)
            except HumiditySensor.DoesNotExist:
                humidity_list.append(0)
                temperature_list.append(0)

        context = {
            'humidity': humidity_list,
            'temperature': temperature_list,
        }

        data = json.dumps(context)
        return HttpResponse(data)


class WaterIrrigation(APIView):
    """
    View to manage the data requests about water irrigation sensors on 'water_irrigation' endpoint.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        """
        It handles the GET request on this endpoint, return an array with water quantity value for each district.
        """
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        water_qty_list = []

        for district in User.DISTRICTS:
            try:
                data = WaterIrrigationSensor.objects.filter(district=district[0])
                count = data.count()
                if count == 0:
                    water_qty_list.append(0)
                else:
                    avg = 0
                    for n in range(count):
                        avg += data[n].water_qty
                    avg /= count
                    water_qty_list.append(avg)
            except WaterIrrigationSensor.DoesNotExist:
                water_qty_list.append(0)

        context = {
            'water_qty': water_qty_list,
        }

        data = json.dumps(context)
        return HttpResponse(data)
