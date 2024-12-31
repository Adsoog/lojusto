from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceItems, ServiceBill, RequestService
from .utils import obtener_estado_condicion

# Señal para recalcular el total_expense cuando se guarde un ServiceItem
@receiver(post_save, sender=ServiceItems)
def update_total_expense(sender, instance, **kwargs):
    request_service = instance.request_service
    # Recalcular el total_expense sumando los total_price de todos los ServiceItems
    total_expense = sum(item.total_price for item in request_service.service_items.all())
    request_service.total_expense = total_expense
    request_service.save()  # Guarda el RequestService con el total actualizado

# Señal para recalcular el total_bills cuando se guarde un ServiceBill
@receiver(post_save, sender=ServiceBill)
def update_total_bills(sender, instance, **kwargs):
    request_service = instance.service_bill
    # Recalcular el total_bills sumando los bill_total de todos los ServiceBills
    total_bills = sum(bill.bill_total for bill in request_service.service_bills.all())
    request_service.total_bills = total_bills
    request_service.save()  # Guarda el RequestService con el total actualizado

@receiver(post_save, sender=ServiceBill)
def actualizar_estado_y_condicion(sender, instance, created, **kwargs):
    """
    Cada vez que se cree o actualice un ServiceBill, se verifica si tiene un RUC
    y, de ser así, se consulta a la API para actualizar is_active (estado) y is_found (condición).
    Evita el bucle infinito al solo guardar cuando haya cambios.
    """
    ruc = instance.bill_ruc
    if not ruc:
        return

    estado, condicion = obtener_estado_condicion(ruc)

    # Asignar valores de cadena basados en la respuesta de la API
    if estado and condicion:
        if estado.upper() in ['ACTIVO', 'INACTIVO'] and condicion.upper() in ['HABIDO', 'NO HABIDO']:
            new_is_active = estado.upper()
            new_is_found = condicion.upper()
        else:
            new_is_active = 'No disponible'
            new_is_found = 'No disponible'
    else:
        new_is_active = 'No disponible'
        new_is_found = 'No disponible'

    # Actualizar solo si hay cambios
    if instance.is_active != new_is_active or instance.is_found != new_is_found:
        ServiceBill.objects.filter(pk=instance.pk).update(is_active=new_is_active, is_found=new_is_found)

    