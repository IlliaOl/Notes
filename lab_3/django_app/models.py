from django.db import models


class CalculateRequest:
    def __init__(self, input_value):
        self.input_value = input_value


class CalculateResponse:
    def __init__(self, result):
        self.output_value = result
