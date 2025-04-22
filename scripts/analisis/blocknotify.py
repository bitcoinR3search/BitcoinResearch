# Este script solo envia el hash del bloque nuevo
# al bot en el raspberrypi2

# El rpi2 corre un servidor API REST que esta escuchando
# la llegada de bloques. esta comunicación no esta cifrada
# y esta limitada para aceptar solo los POST del rpi1
# de la misma manera que rp1 solo acepta solicitudes del rp2

# Para funcionar debe tener permisos y configuraciones en el
# bitcoin.conf de bitcoin-core


import requests
import sys
import os  # Importa el módulo os

def send_block_notification(block_hash):
    url = "http://nodetwo.local:8000/notify"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "hash": block_hash
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado de error
    except requests.exceptions.RequestException:
        os._exit(1)  # Sale del script con un código de salida de 1

    print("Notification sent successfully")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test.py <block_hash>")
        os._exit(1)  # Sale del script con un código de salida de 1

    block_hash = sys.argv[1]
    send_block_notification(block_hash)

if __name__ == "__main__":
    main()
