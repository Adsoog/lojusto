from django import forms
from .models import Area, Laboratory, Vehicle, DailyExchangeRate, Routes

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Nombre del Área'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Descripción del Área',
                'rows': 3
            }),
        }

class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Nombre del Laboratorio'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Descripción del Laboratorio',
                'rows': 3
            }),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'plate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Nombre del Vehículo'
            }),
            'plate': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Placa del Vehículo'
            }),
        }

class DailyExchangeRateForm(forms.ModelForm):
    class Meta:
        model = DailyExchangeRate
        fields = ['date', 'purchase_rate', 'sale_rate']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'border rounded px-3 py-2 w-full'
            }),
            'purchase_rate': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'step': '0.001',
                'placeholder': 'Tasa de Compra'
            }),
            'sale_rate': forms.NumberInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'step': '0.001',
                'placeholder': 'Tasa de Venta'
            }),
        }

class RoutesForm(forms.ModelForm):
    class Meta:
        model = Routes
        fields = ['start_route', 'end_route']
        widgets = {
            'start_route': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Inicio de ruta'
            }),
            'end_route': forms.TextInput(attrs={
                'class': 'border rounded px-3 py-2 w-full',
                'placeholder': 'Fin de de ruta'
            }),
        }