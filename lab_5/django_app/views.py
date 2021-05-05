import logging
from json import dumps, loads
from django.shortcuts import render

import os
import redis
from django.urls import path
from .models import BlackListsModel
from .serializers import BlackListSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict




logger = logging.getLogger('django')
# redis_access = redis.Redis('localhost', port=6379, db=15)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = os.environ.get('REDIS_DB', 15)
redis_access = redis.Redis(redis_host, port=6379, db=15)

class BlackListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queryset = BlackListsModel.objects.all()
        self.serializer_class = BlackListSerializer

    def get(self, request):
        req_type = request.content_type
        if "text" in req_type:
            return render(request, "django_app/request.html")
        elif "json" in req_type:
            id = request.query_params.get('id', None)
            if id is None:
                return Response(status=404)
            else:
                return self.get_details(id)
        else:
            return Response(status=400)

    def post(self, request):
        data = loads(request.body)
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(status=400)
        model = BlackListsModel(**serializer.data)
        model.pk = serializer.data['id']
        model.save()
        redis_access.delete(model.pk)
        return Response(status=200)

    def put(self, request):
        data = loads(request.body)
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response(status=400)
        BlackListsModel(**serializer.data).save()
        return Response(status=201)

    def delete(self, request):
        data = loads(request.body)
        self.queryset.get(pk=data['id']).delete()
        redis_access.delete(data['id'])
        return Response(status=200)

    def get_details(self, pk):
        logger.info(f'[Contacts] getting record with id = {pk}')
        cached = redis_access.get(pk)
        if cached:
            logger.info(f'[Contacts] got record with id = {pk} from redis')
            cached = loads(cached)
            return Response(cached)
        logger.info(f'[Contacts] had to query record with id = {pk} from db')
        obj = self.queryset.get(id=pk)
        if not obj:
            return Response(status=404)
        obj = model_to_dict(obj)
        obj = dumps(obj)
        obj = loads(obj)
        serializer = self.serializer_class(data=obj)
        if not serializer.is_valid():
            return Response(status=404)
        data = serializer.data
        redis_access.set(pk, dumps(data))
        return Response(data)


routes = [
    path('api/blacklist/', BlackListView.as_view())
]
