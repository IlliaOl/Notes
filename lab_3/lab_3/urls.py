from django.contrib import admin
from django.urls import path

from django_app.views import CalculateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculate/', CalculateView.as_view()),
]
