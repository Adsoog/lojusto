from django.shortcuts import render
from perdiems.models import RequestService

# Create your views here.
def index_accounting(request):
    perdiems = RequestService.objects.filter(
        applicant_signature__isnull=False,
        supervisor_signature__isnull=False
    ).exclude(
        applicant_signature='',
        supervisor_signature=''
    )

    return render(request, 'index_accounting.html', {
        'perdiems': perdiems,
    })


# class RequestService(models.Model):
#     area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
#     laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
#     oti = models.CharField(max_length=50)
#     requested_date = models.DateField(auto_now_add=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     days = models.IntegerField()
#     for_interested = models.ForeignKey(Area, related_name='area_interesada', on_delete=models.SET_NULL, null=True, default=1)
#     from_interested = models.ForeignKey(User, related_name='usuario_interesado', on_delete=models.SET_NULL, null=True)
#     persons = models.ManyToManyField(User, related_name='viajantes')
#     motive = models.CharField(max_length=40, default='')
#     details = models.TextField()
#     applicant_signature = models.ImageField(upload_to='signatures/applicant/', null=True, blank=True)
#     supervisor_signature = models.ImageField(upload_to='signatures/supervisor/', null=True, blank=True)
#     accounting_signature = models.ImageField(upload_to='signatures/accounting/', null=True, blank=True)
#     total_bills = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total_expense_dollars = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     state = models.BooleanField(default=False)




# Métodos normales con htmx


# def perdiems_list(request):
#     perdiems = RequestService.objects.all()
#     total_expense_sum = perdiems.aggregate(Sum('total_expense'))['total_expense__sum'] or 0.00
#     bill_total_sum = ServiceBill.objects.aggregate(Sum('bill_total'))['bill_total__sum'] or 0.00
#     total_restante = Decimal(total_expense_sum) - Decimal(bill_total_sum)

#     for perdiem in perdiems:
#         perdiem.total_restante = (Decimal(perdiem.total_expense) if perdiem.total_expense else Decimal(0.00)) - (Decimal(perdiem.total_bills) if perdiem.total_bills else Decimal(0.00))

#     return render(request, 'perdiems/perdiems_list.html', {
#         'perdiems': perdiems,
#     })