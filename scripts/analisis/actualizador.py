# este script tiene funciones para analizar 
# los datos nuevos y bloques.

# esta funcion actualiza la base de datos al valor mas actual
# primero se debe correr el scrip 'recopilador.py' para empezar
# desde el bloque 1. Este proceso demora entre 5 a 6 horas 
# por lo que esta función actualiza al último bloque.
import os
import datetime
import sys
import numpy as np
from time import sleep
from dotenv import load_dotenv
from bitcoinrpc.authproxy import AuthServiceProxy



#os.chdir('D://proyectos//BitcoinResearch//BitcoinResearch//scripts')
os.chdir('/home/ghost/BitcoinResearch/scripts/')
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

load_dotenv('bins/.env')

rpc_user = os.getenv('user')
rpc_pass = os.getenv('pass')  
print(rpc_user,rpc_pass)

def actualizar(user=0,passw=0):
    # este metodo actualiza la db.
    global n_block, time_b, size, ntx, bits, chainwork, strippedsize, weight, total
    flag = True
    # conectarse al nodo
    while(flag):
        try:
            print('Conectando al nodo ... ')
            node = AuthServiceProxy("http://%s:%s@nodeone.local:8332" % (user,passw))
            print('nodo conectado')
            last_block = node.getblockcount()
            last_db_block = int(aux['n_block'][-1])
            print(f'ultimo bloque en red: {last_block}')
            print(f'ultimo bloque en db: {last_db_block}')
            while(last_block!=last_db_block):
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
            #sleep(300)
            sys.exit()

     

actualizar(user=rpc_user,passw=rpc_pass)
