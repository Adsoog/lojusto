from rest_framework import generics, viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from .models import RequestService, ServiceBill, ServiceItems
from .serializers import RequestServiceDetailSerializer, RequestServiceSerializer, ServiceBillSerializer, ServiceItemsSerializer, SimpleRequestServiceSerializer
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Area, Laboratory, Items, RequestService
from .serializers import (
    UserSerializer,
    AreaSerializer,
    LaboratorySerializer,
    ItemsSerializer,
    RequestServiceSerializer,
)
from .forms import ServiceBillForm, RequestServiceForm, ServiceItemsForm, ServiceItemsInlineFormSet
from django.forms import modelformset_factory

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo lectura para listar usuarios (GET /users/) y obtener detalle (GET /users/<id>/).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [permissions.AllowAny]

class LaboratoryViewSet(viewsets.ModelViewSet):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.AllowAny]

class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [permissions.AllowAny]

class RequestServiceViewSet(viewsets.ModelViewSet):
    queryset = RequestService.objects.all()
    serializer_class = RequestServiceSerializer
    permission_classes = [permissions.AllowAny]

class ServiceItemsViewSet(viewsets.ModelViewSet):
    queryset = ServiceItems.objects.all()
    serializer_class = ServiceItemsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Sobrescribe el método create para asociar automáticamente el ServiceItem a un RequestService.
        Se espera que el `request_service_id` se pase como parámetro en la URL.
        """
        request_service_id = request.data.get('request_service_id')
        try:
            request_service = RequestService.objects.get(id=request_service_id)
        except RequestService.DoesNotExist:
            return Response({'error': 'RequestService no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request_service=request_service)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Filtra los ServiceItems por `request_service_id` si se proporciona como parámetro en la URL.
        """
        queryset = ServiceItems.objects.all()
        request_service_id = self.request.query_params.get('request_service_id')
        if request_service_id is not None:
            queryset = queryset.filter(request_service__id=request_service_id)
        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def create_request_service(request):
    if request.method == 'POST':
        serializer = RequestServiceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestServiceListView(ListAPIView):
    queryset = RequestService.objects.all()
    serializer_class = SimpleRequestServiceSerializer
    permission_classes = [permissions.AllowAny]

class RequestServiceDetailView(RetrieveAPIView):
    queryset = RequestService.objects.all()
    serializer_class = RequestServiceDetailSerializer
    permission_classes = [permissions.AllowAny]

class ServiceBillViewSet(viewsets.ModelViewSet):
    queryset = ServiceBill.objects.all()
    serializer_class = ServiceBillSerializer
    permission_classes = [permissions.AllowAny]  

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# Métodos normales con htmx
def perdiems_list(request):
    perdiems = RequestService.objects.all()
    total_expense_sum = perdiems.aggregate(Sum('total_expense'))['total_expense__sum'] or 0.00
    bill_total_sum = ServiceBill.objects.aggregate(Sum('bill_total'))['bill_total__sum'] or 0.00
    total_restante = Decimal(total_expense_sum) - Decimal(bill_total_sum)

    for perdiem in perdiems:
        perdiem.total_restante = (Decimal(perdiem.total_expense) if perdiem.total_expense else Decimal(0.00)) - (Decimal(perdiem.total_bills) if perdiem.total_bills else Decimal(0.00))

    return render(request, 'perdiems/perdiems_list.html', {
        'perdiems': perdiems,
    })

def create_request_service(request):
    if request.method == 'POST':
        request_service_form = RequestServiceForm(request.POST, request.FILES)
        service_items_formset = ServiceItemsInlineFormSet(request.POST, prefix='service_items')

        if request_service_form.is_valid() and service_items_formset.is_valid():
            request_service = request_service_form.save()

            service_items_formset.instance = request_service
            service_items_formset.save()

            return redirect('perdiems_list')
        else:
            print("Formulario principal errores:", request_service_form.errors)
            print("Formset errores:", service_items_formset.errors)
    else:
        request_service_form = RequestServiceForm()
        service_items_formset = ServiceItemsInlineFormSet(queryset=ServiceItems.objects.none(), prefix='service_items')

    return render(request, 'perdiems/perdiem_form.html', {
        'request_service_form': request_service_form,
        'service_items_formset': service_items_formset,
    })

def perdiem_detail(request, id):
    perdiem = get_object_or_404(RequestService, id=id)
    bills = ServiceBill.objects.filter(service_bill=perdiem)
    
    total_rendido = bills.aggregate(Sum('bill_total'))['bill_total__sum'] or 0.00
    total_rendido = Decimal(total_rendido) 
    
    total_restante = perdiem.total_expense - total_rendido
    
    return render(request, 'perdiems/perdiem_detail.html', {
        'perdiem': perdiem,
        'bills': bills,
        'total_rendido': total_rendido,
        'total_restante': total_restante
    })

def toggle_signature(request, signature_type, id):
    perdiem = get_object_or_404(RequestService, id=id)
    employee = request.user.employee  
    
    if signature_type == 'applicant':
        if not perdiem.applicant_signature: 
            perdiem.applicant_signature = employee.signature
        else:
            perdiem.applicant_signature = None
        perdiem.save()

    elif signature_type == 'supervisor':
        if not perdiem.supervisor_signature:
            perdiem.supervisor_signature = employee.signature
        else:
            perdiem.supervisor_signature = None
        perdiem.save()

    elif signature_type == 'accounting':
        if not perdiem.accounting_signature:
            perdiem.accounting_signature = employee.signature
        else:
            perdiem.accounting_signature = None
        perdiem.save()

    return render(request, 'partials/signature_partial.html', {'perdiem': perdiem})

def perdiem_bills(request, id):
    perdiem = get_object_or_404(RequestService, id=id)
    bills = ServiceBill.objects.filter(service_bill=perdiem)
    
    return render(request, 'perdiems/perdiem_bills.html', {'perdiem': perdiem, 'bills': bills})

def bill_form(request, bill_id):
    bill = get_object_or_404(ServiceBill, id=bill_id)
    form = ServiceBillForm(request.POST or None, request.FILES or None, instance=bill)

    if form.is_valid():
        form.save()
        request_service = bill.service_bill
        return redirect('perdiem_bills', id=request_service.id)

    return render(request, 'partials/bill_form.html', {'form': form, 'bill': bill})
