# perdiems/utils.py
import requests

def obtener_estado_condicion(ruc):
    url = f"https://api.apis.net.pe/v2/sunat/ruc?numero={ruc}"
    token = "apis-token-12335.66f3s7HjN6Nel8gcQOHo0le531JKyeMB"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    try:
        response = requests.get(url, headers=headers)
        # Asegúrate de que la respuesta sea en formato UTF-8
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            estado = data.get('estado', 'No disponible')  # e.g. "ACTIVO" / "INACTIVO"
            condicion = data.get('condicion', 'No disponible')  # e.g. "HABIDO" / "NO HABIDO"
            print(data, estado, condicion)
            return estado, condicion
        else:
            print(f"Error {response.status_code}: No se pudo obtener información del RUC {ruc}.")
            return None, None
    except Exception as e:
        print(f"Se produjo un error al consultar el RUC {ruc}: {e}")
        return None, None