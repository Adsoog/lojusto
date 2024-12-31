from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Laboratory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    plate = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.plate})"

class DailyExchangeRate(models.Model):
    date = models.DateField(unique=True)
    purchase_rate = models.DecimalField(max_digits=6, decimal_places=3)
    sale_rate = models.DecimalField(max_digits=6, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | Compra: {self.purchase_rate} | Venta: {self.sale_rate}"

class Routes(models.Model):
    start_route = models.CharField(max_length=20, default='')
    end_route = models.CharField(max_length=20, default='')
    
    def __str__(self):
        return f"Inicio de ruta: {self.start_route} - Fin de ruta: {self.end_route}"