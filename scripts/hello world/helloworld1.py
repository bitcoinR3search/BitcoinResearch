"""
Este script es de prueba para ver si conecta al nodo
y esta configurado 
"""
import os
from bitcoin.rpc import RawProxy
from pprint import pprint
from dotenv import load_dotenv



load_dotenv('/home/ghost/.env')


# RPC remote procedure call
rpc_user = os.getenv('user')
rpc_password = os.getenv('pass')
p = RawProxy(service_url='http://%s:%s@nodeone.local:8332' %
             (rpc_user, rpc_password))

info = p.getblockchaininfo()

pprint(info)
