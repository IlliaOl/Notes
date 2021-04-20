from django.contrib import admin
from django.urls import path

from django_app.views import routes

urlpatterns = [
    path('admin/', admin.site.urls),
] + routes
