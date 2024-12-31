from django.db import models
from django.contrib.auth.models import User
from general.models import Area, Laboratory

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    dni = models.IntegerField()
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    
    def __str__(self):
        return f"Employee: {self.user.username}, Area: {self.area.name}"