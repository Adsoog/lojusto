# views.py
from django.shortcuts import render

def home(request):
    links = [
        {"href": "/productos", "icon": "conta.svg", "title": "Productos"},
        {"href": "/ventas", "icon": "crm.svg", "title": "Ventas"},
        {"href": "/finanzas", "icon": "documentos.svg", "title": "Finanzas"},
        {"href": "/inventario", "icon": "icon.svg", "title": "Inventario"},
        {"href": "/viaticos/lista", "icon": "marketingsocial.svg", "title": "Viáticos"}
    ]
 
    return render(request, 'home/home.html', {'links': links})
