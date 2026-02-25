from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/notes/', views.notes_api, name='notes-api'),
]
