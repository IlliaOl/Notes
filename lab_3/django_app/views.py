from json import loads
from django.shortcuts import render

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django_app.models import CalculateResponse, CalculateRequest
from django_app.serializers import CalculationResponseSerializer, CalculationRequestSerializer
from django_app.utils import Calculator


class CalculateView(APIView):

    def post(self, request):
        parsed_request = loads(request.body)
        request_data_serializer = CalculationRequestSerializer(data=parsed_request)
        if not request_data_serializer.is_valid():
            return Response(status=400)
        request_data = CalculateRequest(**request_data_serializer.validated_data)
        calculation_result = Calculator.calculate(request_data.input_value)
        response_data = CalculateResponse(calculation_result)
        response_data_serializer = CalculationResponseSerializer(response_data)
        response = Response(response_data_serializer.data)
        return response

    def get(self, request):
        return render(request, "django_app/request.html")





