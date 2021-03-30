from rest_framework import serializers


class CalculationRequestSerializer(serializers.Serializer):
    input_value = serializers.DecimalField(max_digits=19, decimal_places=10)


class CalculationResponseSerializer(serializers.Serializer):
    output_value = serializers.DecimalField(max_digits=19, decimal_places=2)