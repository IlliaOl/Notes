from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView
from notes import views

urlpatterns = [

    path('users/', include('users.urls')), 
    path('users/', include('django.contrib.auth.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    path('', include('notes.urls')),

]
