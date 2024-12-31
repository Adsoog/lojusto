from django.shortcuts import render, get_object_or_404, redirect
from .models import Area, Laboratory, Vehicle, DailyExchangeRate, Routes
from .forms import AreaForm, LaboratoryForm, VehicleForm, DailyExchangeRateForm, RoutesForm

# Create your views here.
def index_general(request):
    areas = Area.objects.all()
    laboratories = Laboratory.objects.all()
    vehicles = Vehicle.objects.all()
    exchange_rates = DailyExchangeRate.objects.all()
    routes = Routes.objects.all()

    return render(request, 'index_general.html',{
        'areas': areas,
        'laboratories' : laboratories,
        'vehicles' : vehicles,
        'routes' : routes
    })

def create_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_general')
    else:
        form = AreaForm()
    return render(request, 'forms/create_area.html', {'form': form})

def create_laboratory(request):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_general')
    else:
        form = LaboratoryForm()
    return render(request, 'forms/create_laboratory.html', {'form': form})

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_general')
    else:
        form = VehicleForm()
    return render(request, 'forms/create_vehicle.html', {'form': form})

def create_route(request):
    if request.method == 'POST':
        form = RoutesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_general')
    else:
        form = RoutesForm() 
    return render(request, 'forms/create_route.html', {'form': form})

def create_exchange_rate(request):
    if request.method == 'POST':
        form = DailyExchangeRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_general')
    else:
        form = DailyExchangeRateForm()
    return render(request, 'forms/create_exchange_rate.html', {'form': form})