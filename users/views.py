from django.shortcuts import render
from .models import Employee
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, EmployeeSerializer, GroupSerializer

# Create your views here.
def employees(render):
    pass

class UserViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows employees to be viewed or edited.
    """
    queryset = Employee.objects.all().order_by('user__date_joined')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows employees to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]