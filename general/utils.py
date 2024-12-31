# utils.py
import requests
from datetime import date
from decimal import Decimal
from .models import DailyExchangeRate

def obtener_tipo_cambio_sunat():
    """
    Llama a la API de apis.net.pe para obtener el tipo de cambio 
    USD -> PEN del día actual. 
    Retorna (compra, venta) o (None, None) si falla.
    """
    url = "https://api.apis.net.pe/v2/sunat/tipo-cambio"
    token = "apis-token-12335.66f3s7HjN6Nel8gcQOHo0le531JKyeMB"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            compra = data.get('precioCompra') 
            venta = data.get('precioVenta') 
            
            print("Respuesta de la API:", data)  
            print("Valores extraídos:", compra, venta)
            
            return compra, venta
        else:
            print(f"Error {response.status_code}: No se pudo obtener el tipo de cambio.")
            return None, None
    except Exception as e:
        print(f"Error al consultar tipo de cambio: {e}")
        return None, None

def get_or_create_today_exchange_rate():
    """ 
    Retorna la tasa de venta del día actual; la crea si no existe aún.
    """
    hoy = date.today()
    daily_rate = DailyExchangeRate.objects.filter(date=hoy).first()

    if not daily_rate:
        compra, venta = obtener_tipo_cambio_sunat() 
        if compra and venta:
            daily_rate = DailyExchangeRate.objects.create(
                date=hoy,
                purchase_rate=Decimal(compra),
                sale_rate=Decimal(venta)
            )

    if daily_rate:
        return daily_rate.sale_rate
    return None
