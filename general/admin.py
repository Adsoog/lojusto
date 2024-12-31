from django.contrib import admin
from .models import Area, Laboratory, Vehicle, DailyExchangeRate

# Registrar el modelo Area en el Admin
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Mostrar nombre y descripción
    search_fields = ('name',)  # Permitir búsqueda por nombre

# Registrar el modelo Laboratory en el Admin
@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Registrar el modelo Vehicle en el Admin
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'plate')  # Mostrar nombre y placa del vehículo
    search_fields = ('name', 'plate')  # Permitir búsqueda por nombre y placa

@admin.register(DailyExchangeRate)
class DailyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'purchase_rate', 'sale_rate', 'created_at')
    search_fields = ('date', 'purchase_rate', 'sale_rate', 'created_at')



