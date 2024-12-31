from django.contrib import admin
from .models import RequestService, ServiceItems, Items, ServiceBill

@admin.register(RequestService)
class RequestServiceAdmin(admin.ModelAdmin):
    list_display = ('oti', 'requested_date', 'start_date', 'end_date', 'total_expense', 'total_bills')
    search_fields = ('oti',)

@admin.register(ServiceItems)
class ServiceItemsAdmin(admin.ModelAdmin):
    list_display = ('request_service', 'items', 'price')
    search_fields = ('request_service__oti',)
    exclude = ('amount', 'total_price') 

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('item', 'amount_per_day', 'type_item')
    search_fields = ('item',)

@admin.register(ServiceBill)
class ServiceBillAdmin(admin.ModelAdmin):
    list_display = ('service_bill', 'bill_number', 'bill_total', 'bill_date')
    search_fields = ('bill_number',)
