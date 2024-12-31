from django.contrib import admin
from .models import Employee

# Register your models here.
# Registrar el modelo Area en el Admin
@admin.register(Employee)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('user', 'area', 'laboratory', 'dni', 'signature')  
    search_fields = ('user',)