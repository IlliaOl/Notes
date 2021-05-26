from django.urls import path

from .views import List, Create, HomePage, Delete, Update
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('notes/', List.as_view(), name='note_list'),
    path('new/', Create.as_view(), name='note_new'),
    path('<int:pk>/delete/',
         Delete.as_view(), name='note_delete'),
    path('<int:pk>/edit/',
         Update.as_view(), name='note_edit'),

]