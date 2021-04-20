from rest_framework import serializers
from .models import BlackListModel


class BlackListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BlackListModel
        fields = '__all__'
