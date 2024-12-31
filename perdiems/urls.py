# path('viaticos/', include('perdiems.urls'))
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestServiceListView, ServiceItemsViewSet, create_request_service, perdiems_list, ServiceBillViewSet, RequestServiceViewSet
from . import views
from .views import (
    UserViewSet,
    AreaViewSet,
    LaboratoryViewSet,
    ItemsViewSet,
    RequestServiceViewSet,
    RequestServiceDetailView,
)

router = DefaultRouter()
# Registramos el ViewSet con el nombre que desees (service-bills, bills, etc.)
router.register(r'service-bills', ServiceBillViewSet, basename='servicebill')
router.register(r'users', UserViewSet, basename='user')
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'laboratories', LaboratoryViewSet, basename='laboratory')
router.register(r'items', ItemsViewSet, basename='item')
router.register(r'request-services', RequestServiceViewSet, basename='requestservice')
router.register(r'service-items', ServiceItemsViewSet, basename='service-item')

urlpatterns = [
    path('', include(router.urls)),
    path('create-request-service/', create_request_service, name='create-request-service'),
    path('list-request-services/', RequestServiceListView.as_view(), name='request-service-list'),
    path('request-services/<int:pk>/detail/', RequestServiceDetailView.as_view(), name='requestservice-detail'),
    path('lista/', views.perdiems_list, name='perdiems_list'),
    path('viaticos/<int:id>/', views.perdiem_detail, name='perdiem_detail'),
    path('viaticos/facturas/<int:id>/', views.perdiem_bills, name='perdiem_bills'),
    path('viaticos/<str:signature_type>/<int:id>/', views.toggle_signature, name='toggle_signature'),
    path('facturas-viaticos/<int:bill_id>/', views.bill_form, name='bill_form'),

]   

htmxpatterns = [
    path('create-request-service/', views.create_request_service, name='create_request_service'),

]

urlpatterns += htmxpatterns