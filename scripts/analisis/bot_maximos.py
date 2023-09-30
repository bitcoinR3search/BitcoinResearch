# Este bot verifica en cada bloque nuevo 
# los valores maximos y registra el dato
# numero de tx, dificultad max, anomalia de tiempo
# tiempo record de llegada de un bloque (max)


# formas de solución:

# 1 crear un crontab cada 11 min 
# 2 nodo te avisa cuando llega un nuevo bloque   <--

import numpy as np
import sys
import os 
from app.readata import leer_data, last_block
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy

os.chdir('D:\proyectos\BitcoinResearch\BitcoinResearch\scripts')
load_dotenv('analisis/.env')

rpc_user = os.getenv('user')
rpc_password = os.getenv('pass')

try:
    node =  AuthServiceProxy(
        "http://%s:%s@nodeone.local:8332" % (rpc_user, rpc_password))
        # si todo esta ok y el nodo esta online acepta sesion
except:
        # si el nodo esta offline o no se logra autentificar
    sys.exit()


last_block = last_block()
hash_last_block = node.getblockhash(last_block)
block = node.getblock(hash_last_block)
a, b, c = block['nTx'], block['bits'], block['time']

# obtenemos los valores maximos

n_block,time,ntx = leer_data('n_block','time_b','ntx')

# Obtenemos el maximo de ntx

max_ntx = np.max(np.array(ntx))
print(max_ntx)


# # if nuevo_max > max_registro:
# #     #ejecutasr script: ntx.py