from django import forms
from .models import ServiceBill, RequestService, ServiceItems, Items
from django.forms import inlineformset_factory

class ServiceBillForm(forms.ModelForm):
    class Meta:
        model = ServiceBill
        fields = [
            'service_bill', 
            'bill_image', 
            'bill_ruc', 
            'bill_emisor', 
            'bill_number', 
            'bill_date', 
            'bill_total', 
            'bill_details',
            'bill_type',
            'bill_class',
            'is_active', 
            'is_found',
        ]
        widgets = {
            'service_bill': forms.Select(attrs={
                'class': 'border rounded px-3 py-2 w-full',
            }),
            'bill_image': forms.FileInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
            }),
            'bill_ruc': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'RUC del Emisor',
            }),
            'bill_emisor': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Nombre del Emisor',
            }),
            'bill_number': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Número de Factura',
            }),
            'bill_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded px-3 py-2 w-full',
            }),
            'bill_total': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Total',
                'step': '0.01',
            }),
            'bill_details': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Detalles de la factura',
                'rows': 3,
            }),
            'bill_type': forms.Select(attrs={
                'class': 'border rounded px-3 py-2 w-full',
            }),
            'bill_class': forms.Select(attrs={
                'class': 'border rounded px-3 py-2 w-full',
            }),
            'is_active': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Estado',
            }),
            'is_found': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Condición',
            }),
        }

# Formulario para la solicitud de viáticos
class RequestServiceForm(forms.ModelForm):
    class Meta:
        model = RequestService
        fields = [
            'area', 'laboratory', 'oti', 'start_date', 'end_date', 'days',
            'for_interested', 'from_interested', 'persons', 'details',
            'total_bills', 'total_expense'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'oti': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'laboratory': forms.Select(attrs={'class': 'form-control'}),
            'for_interested': forms.Select(attrs={'class': 'form-control'}),
            'from_interested': forms.Select(attrs={'class': 'form-control'}),
            'persons': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para los ítems de la solicitud de viáticos
class ServiceItemsForm(forms.ModelForm):
    class Meta:
        model = ServiceItems
        fields = ['items', 'price']
        widgets = {
            'items': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formset en línea para los ítems del servicio
ServiceItemsInlineFormSet = inlineformset_factory(
    RequestService,
    ServiceItems,
    form=ServiceItemsForm,  # Especificar el formulario personalizado
    fields=['items', 'price'],
    extra=1,
    can_delete=True,
)

#https://justdjango.com/blog/dynamic-forms-in-django-htmx