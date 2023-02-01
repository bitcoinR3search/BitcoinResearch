# Este script es un ejemplo de como se puede
# recopilar data del bitcoin usando el nodo


from bitcoin.rpc import RawProxy
from dotenv import load_dotenv
import os
from pprint import pprint

# cargamos variables de autentificacion
load_dotenv('.env')
rpc_user=  os.getenv('user')
rpc_password=os.getenv('pass')

# autentificación
rpc_connection = RawProxy(service_url='http://%s:%s@nodebtc.local:8332'%(rpc_user, rpc_password))


# Se analiza por grupos de 100 bloques

a = rpc_connection.getblockcount() 
pprint(a)