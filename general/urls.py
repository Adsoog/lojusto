from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_general, name='index_general'),
]

htmxpatters = [
    path('crear-area', views.create_area, name='create_area'),
    path('crear-laboratorio', views.create_laboratory, name='create_lab'),
    path('crear-vehiculo', views.create_vehicle, name='create_vehicle'),
    path('crear-ruta', views.create_route, name='create_route'),
]
    
urlpatterns += htmxpatters