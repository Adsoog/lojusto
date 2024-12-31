# perdiems/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_accounting, name="index_accounting"),
]
