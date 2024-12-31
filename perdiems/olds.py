class Route(models.Model):
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)

    def __str__(self):
        return f"DE: {self.start_location} A: {self.end_location}"

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'

class TravelTickets(models.Model):
    TICKETS_CHOICES = [
        ('terrestre', 'Terrestre'),
        ('vuelo', 'Vuelo'),
        ('otros', 'Otros')
    ]
    tickets_type = models.CharField(max_length=50, choices=TICKETS_CHOICES, default='terrestre')

    class Meta:
        verbose_name = 'Boleto de viaje'
        verbose_name_plural = 'Boletos de viaje'

class PerdiemTicket(models.Model):
    CURRENCY_CHOICES = [
        ('S/', 'Soles'),
        ('$', 'Dólares'),
    ]
    perdiem_request = models.ForeignKey('PerDiemRequest', on_delete=models.CASCADE)
    travel_ticket = models.ForeignKey(TravelTickets, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='S/'
    )