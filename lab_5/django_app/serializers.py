from rest_framework import serializers
from .models import BlackListsModel


class BlackListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BlackListsModel
        fields = '__all__'
