"""
DEPRECATED

Este script es de prueba para ver si conecta al nodo
y esta configurado 
"""
import os
from bitcoin.rpc import RawProxy
from pprint import pprint
from dotenv import load_dotenv

os.chdir('D:\proyectos\BitcoinResearch\BitcoinResearch\scripts')

#load_dotenv('/home/ghost/.env')
load_dotenv('/analisis/.env')


# # RPC remote procedure call
# rpc_user = os.getenv('user')
# print(rpc_user)
# rpc_password = os.getenv('pass')
# #p = RawProxy(service_url='http://%s:%s@nodeone.local:8332' %
# #             (rpc_user, rpc_password))


p = RawProxy(service_url='http://%s:%s@192.168.1.4:8332' %
             (rpc_user, rpc_password))


# info = p.getblockchaininfo()

# pprint(info)
