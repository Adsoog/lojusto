from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from django.forms import ValidationError
from users.models import Employee
from general.models import Area, Laboratory, Vehicle
from general.utils import get_or_create_today_exchange_rate

class Items(models.Model):
    ITEMS_CHOICES = [
        ('alimentacion', 'Alimentación'),
        ('transporte', 'Transporte'),
        ('alojamiento', 'Alojamiento'),
        ('combustible', 'Combustible'),
        ('reparaciones', 'Reparaciones'),
        ('otros', 'Otros'),
    ]
    item = models.CharField(max_length=50, choices=ITEMS_CHOICES)
    amount_per_day = models.IntegerField(default=1)
    type_item = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.item} - cantidad por dia: {self.amount_per_day}"

class RequestService(models.Model):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    oti = models.CharField(max_length=50)
    requested_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField()
    for_interested = models.ForeignKey(Area, related_name='area_interesada', on_delete=models.SET_NULL, null=True, default=1)
    from_interested = models.ForeignKey(User, related_name='usuario_interesado', on_delete=models.SET_NULL, null=True)
    persons = models.ManyToManyField(User, related_name='viajantes')
    motive = models.CharField(max_length=40, default='')
    details = models.TextField()
    applicant_signature = models.ImageField(upload_to='signatures/applicant/', null=True, blank=True)
    supervisor_signature = models.ImageField(upload_to='signatures/supervisor/', null=True, blank=True)
    accounting_signature = models.ImageField(upload_to='signatures/accounting/', null=True, blank=True)
    total_bills = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_expense_dollars = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):

        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.days = delta.days + 1

        if self.from_interested:
            try:
                employee = self.from_interested.employee
                if employee.signature:
                    self.applicant_signature_image = employee.signature
            except Employee.DoesNotExist:
                raise ValidationError("El usuario no tiene una firma registrada.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.details} - ORI: {self.oti}"

class ServiceItems(models.Model):
    request_service = models.ForeignKey(RequestService, related_name='service_items', on_delete=models.CASCADE)
    items = models.ForeignKey(Items, related_name='service_item', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(blank=True, null=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        amount_per_day = self.items.amount_per_day 
        days = self.request_service.days
        self.amount = amount_per_day * days
        self.total_price = self.price * self.amount 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.items}"

class ServiceBill(models.Model):
    BILL_TYPE_CHOICES = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
        ('RECIBO', 'Recibo'),
        ('TICKET', 'Ticket'),
        ('PLANILLA_MOVILIDAD', 'Planilla movilidad'),
    ]
    
    BILL_CLASS_CHOICES = [
        ('ALIMENTACION', 'Alimentacion'),
        ('HOSPEDAJE', 'Hospedaje'),
        ('GASOLINA', 'GASOLINA'),
        ('PASAJE', 'Pasaje')
    ]

    service_bill = models.ForeignKey(RequestService, on_delete=models.CASCADE, related_name='service_bills', null=True, blank=True)
    bill_image = models.ImageField(upload_to="bills/", null=True, blank=True)
    bill_ruc = models.BigIntegerField(null=True, blank=True)
    bill_emisor = models.CharField(max_length=100, null=True, blank=True)
    bill_number = models.CharField(max_length=50, null=True, blank=True)
    bill_date = models.DateField(null=True, blank=True)
    bill_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    bill_details = models.TextField(null=True, blank=True)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, null=True, blank=True)
    bill_class = models.CharField(max_length=20, choices=BILL_CLASS_CHOICES, null=True, blank=True)
    is_active = models.CharField(max_length=50, null=True, blank=True)
    is_found = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Factura {self.bill_number} de {self.bill_total} soles"

