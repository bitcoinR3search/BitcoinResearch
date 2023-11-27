
import os
import datetime
import requests
import numpy as np
import pandas as pd
from time import sleep
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy
#esta libreria se carga desde el otro script que invoca
#por eso lleva app.readata
from app.readata import time_data, leer_data
os.chdir('/home/ghost/BitcoinResearch/scripts/')
load_dotenv('bins/.env')

user = os.getenv('user')
passw = os.getenv('pass')  

print('Actualizando la DB')

aux = np.load('bins/database.npz', allow_pickle='TRUE')
n_block = aux['n_block']
time_b = aux['time_b']
size = aux['size']
ntx = aux['ntx']
bits = aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']
total = aux['total']
flag = True
print(f'last block en db {int(n_block[-1])}')
# conectarse al nodo
while(flag):
    try:
        print('Conectando al nodo ... ')
        node = AuthServiceProxy("http://%s:%s@nodeone.local:8332" % (user,passw))
        print('nodo conectado')
        last_block = node.getblockcount()
        last_db_block = int(aux['n_block'][-1])
        print(f'last block en red {last_block}')
        
        if(last_block==last_db_block):
            print('Todo sinctronizado')
            break
        else: pass
        while(last_block!=last_db_block):
            print('Actualizando ...')
            #este bucle recopila rapidamente los valores del DB
            print(f'Nuevo bloque encontrado {last_db_block+1}')
            hash = node.getblockhash(last_db_block+1)
            block = node.getblock(hash)
            a_b, b, c, d, e, f, g, h = block['height'], block['time'], block['size'], block['nTx'], block['bits'], block['chainwork'], block['strippedsize'], block['weight']
            n_block=np.append(n_block, a_b)
            date = datetime.datetime.utcfromtimestamp(b).strftime('%Y-%m-%d %H:%M:%S')
            time_b=np.append(time_b, date)
            size=np.append(size, c)
            ntx=np.append(ntx, d)
            bits=np.append(bits, e)
            chainwork=np.append(chainwork, f)
            strippedsize=np.append(strippedsize, g)
            weight=np.append(weight, h)
            last_db_block+=1
            last_block = node.getblockcount()
            sleep(1)
        print(f'Actualizado a {last_block}')
        general = node.getblockchaininfo()          
        total_size = general['size_on_disk']
        print('Guardando DB, no cancele hasta que termine')
        np.savez('bins/database.npz', n_block=n_block, time_b=time_b, size=size, ntx=ntx, bits=bits,chainwork=chainwork, strippedsize=strippedsize, weight=weight, total=total_size)
        print('Guardado finalizado')
        flag=False
    except:
        # si el nodo no esta funcionando espera 
        # 5 minutos antes de volver a intentarlo
        print('error autentificando al nodo')
        print('Probando otra vez en 5 min...')
        sleep(300)
