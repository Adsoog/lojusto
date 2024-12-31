from rest_framework import serializers
from general.models import Area, Laboratory
from .models import Items, ServiceItems, RequestService, ServiceBill
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RequestService, ServiceItems, Items


# 1. Serializer para User (para poder listar y elegir en persons, from_interested, etc.)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# 2. Serializer para Area
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'description']

# 3. Serializer para Laboratory
class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ['id', 'name', 'description']

# 4. Serializer para Items
class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'item', 'amount_per_day', 'type_item']

class ServiceItemsSerializer(serializers.ModelSerializer):
    # Campo para escritura: acepta solo el ID del item
    items = serializers.PrimaryKeyRelatedField(
        queryset=Items.objects.all()
    )

    class Meta:
        model = ServiceItems
        fields = ['id', 'items', 'price', 'amount', 'total_price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Reemplaza el ID del ítem con los detalles del ítem
        representation['items'] = ItemsSerializer(instance.items).data
        return representation

    def create(self, validated_data):
        # Extrae los datos de 'items' ya que 'items_detail' es solo de lectura
        items = validated_data.pop('items')
        service_item = ServiceItems.objects.create(items=items, **validated_data)
        return service_item

    def update(self, instance, validated_data):
        # Actualiza los campos necesarios
        items = validated_data.pop('items', None)
        if items is not None:
            instance.items = items
        instance.price = validated_data.get('price', instance.price)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        return instance
        
# 6. Serializer para RequestService (con service_items anidados)
class RequestServiceSerializer(serializers.ModelSerializer):
    """
    Maneja la creación/actualización de RequestService
    con sus ServiceItems de manera anidada.
    """
    area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    laboratory = serializers.PrimaryKeyRelatedField(queryset=Laboratory.objects.all())
    for_interested = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
    from_interested = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    persons = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = RequestService
        fields = [
            'id',
            'area',
            'laboratory',
            'oti',
            'requested_date',
            'start_date',
            'end_date',
            'days',
            'for_interested',
            'from_interested',
            'persons',
            'details',
            'applicant_signature',
            'supervisor_signature',
            'accounting_signature',
            'total_bills',
            'total_expense',
            'total_expense_dollars',
        ]

    def create(self, validated_data):
        # Sacamos la lista de persons del validated_data
        persons_data = validated_data.pop('persons', [])

        # Creamos el RequestService sin el campo persons (porque es ManyToMany)
        request_service = RequestService.objects.create(**validated_data)

        # Asignamos la relación ManyToMany a persons mediante .set(...)
        if persons_data:
            request_service.persons.set(persons_data)

        return request_service

    def update(self, instance, validated_data):
        persons_data = validated_data.pop('persons', [])
        service_items_data = validated_data.pop('service_items', [])

        # Actualizas campos normales
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Actualizar ManyToMany
        if persons_data:
            instance.persons.set(persons_data)
        else:
            instance.persons.clear()

        return instance
    
# Serializer de Detalle para RequestService
class RequestServiceDetailSerializer(serializers.ModelSerializer):
    # Anidamos la información de las relaciones 
    area = AreaSerializer(read_only=True)
    laboratory = LaboratorySerializer(read_only=True)
    for_interested = AreaSerializer(read_only=True)
    from_interested = UserSerializer(read_only=True)
    persons = UserSerializer(many=True, read_only=True)

    # Si quieres también ver sus ServiceItems en el detalle
    service_items = ServiceItemsSerializer(many=True, read_only=True)

    class Meta:
        model = RequestService
        fields = [
            'id',
            'area',
            'laboratory',
            'oti',
            'requested_date',
            'start_date',
            'end_date',
            'days',
            'for_interested',
            'from_interested',
            'persons',
            'details',
            'applicant_signature',
            'supervisor_signature',
            'accounting_signature',
            'total_bills',
            'total_expense',
            'total_expense_dollars',
            'service_items',  # <- si lo deseas ver
        ]

class SimpleRequestServiceSerializer(serializers.ModelSerializer):
    total_bills = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    total_expense_dollars = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = RequestService
        fields = [
            'id',
            'oti', 
            'requested_date', 
            'start_date', 
            'end_date', 
            'details', 
            'applicant_signature', 
            'supervisor_signature',
            'accounting_signature', 
            'total_bills', 
            'total_expense', 
            'total_expense_dollars'
        ]

class ServiceBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBill
        fields = [
            'id',
            'service_bill',
            'bill_image',
            'bill_ruc',
            'bill_emisor',
            'bill_number',
            'bill_date',
            'bill_total',
            'bill_details',
            'is_active',
            'is_found'
        ]


