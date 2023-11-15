# este script tiene funciones para analizar 
# los datos nuevos y bloques.

# esta funcion actualiza la base de datos al valor mas actual
# primero se debe correr el scrip 'recopilador.py' para empezar
# desde el bloque 1. Este proceso demora entre 5 a 6 horas 
# por lo que esta función actualiza al último bloque.
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

#os.chdir('D://proyectos//BitcoinResearch//BitcoinResearch//scripts')
os.chdir('/home/ghost/BitcoinResearch/scripts/')

load_dotenv('bins/.env')

rpc_user = os.getenv('user')
rpc_pass = os.getenv('pass')  



def actualizar(user=rpc_user,passw=rpc_pass):
    # este metodo actualiza la db.
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
                return 
            else: pass
            while(last_block!=last_db_block):
                print('Antualizando ...')
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


def bits_to_difficulty(bits):
        bits = int(bits, 16)
        # Convertir bits a un número de 256 bits en formato big-endian
        target = (bits & 0x007fffff) * 2 ** (8 * ((bits >> 24) - 3))
        # Calcular la dificultad como el cociente entre el objetivo máximo y el objetivo actual
        max_target = 0xffff * 2 ** (8 * (0x1d - 3))
        difficulty = max_target / target
        return difficulty


def data_metrics():
    #al llamar a esta función los valores ya estaran actualizados.
    if(os.path.exists('bins/ath.npz')):
         return print('ath database existe')
    else:
        print('calculando ATH')
        aux = np.load('bins/database.npz', allow_pickle='TRUE')
        print('Calculando ATH en DB')
        #solo nos es de interes:
        time_b = aux['time_b']
        bits = aux['bits']
        difficulty = np.array([bits_to_difficulty(a) for a in bits])
        chainw=aux['chainwork']
        time_block = pd.Series(pd.to_datetime(time_b)).diff().dt.total_seconds().dropna().replace(0, 1)
        window=1008
        chainwork = pd.Series([int(a,16) for a in chainw]).diff().dropna()
        hashrate  = pd.Series([(chainwork[a]/1e18)/time_block[a] for a in range(1,len(time_block)+1)])
        hashrate_smoothed = hashrate.rolling(window).median().fillna(np.mean(hashrate[:window]))

        hashrate_ath = hashrate_smoothed.max()
        time_ath = time_block.max()
        time_ath_halv = time_block[3*210000:].max()
        dif_ath = difficulty.max()
        np.savez('bins/ath.npz', hash=hashrate_ath,time_total=time_ath,time_halv=time_ath_halv,dif=dif_ath)
        return print('Guardado en disco')


def alerta(n=0,data=0):
    url = "http://nodeone.local:8001/notify"
    headers = {"accept": "application/json",
    "Content-Type": "application/json"}
    alerta_tipo = ['hashrate','time_b total','time_b halv','difficulty']
    data = {"tipo": alerta_tipo[n] , "data":data}
    try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de estado de error
            print("Notification sent successfully")

    except requests.exceptions.RequestException:
            print('Servidor 2 OFFLINE')

def analisis(hash=0,user=rpc_user,passw=rpc_pass):
    #con el nuevo hash debemos volver a consultar al nodo
    print('analizando nuevo bloque')
    flag=True
    while(flag):
        try:
            print('Conectando al nodo ... ')
            node = AuthServiceProxy("http://%s:%s@nodeone.local:8332" % (user,passw))
            print('nodo conectado')
            block = node.getblock(hash)
            flag=False
        except:
            # si el nodo no esta funcionando espera 
            # 5 minutos antes de volver a intentarlo
            print('error autentificando al nodo')
            print('Probando otra vez en 5 min...')
            sleep(300)
    aux = np.load('bins/ath.npz',allow_pickle='TRUE')
    print('Buscando ATH en bloque...')
    #buscamos el valor de hashrate
    chainw, timestamp = leer_data('chainwork','time_b')
    np.append(chainw,block['chainwork'])
    date = datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d %H:%M:%S')
    np.append(timestamp,date)
    time_block = pd.Series(pd.to_datetime(timestamp)).diff().dt.total_seconds().dropna().replace(0, 1)
    window=1008
    chainwork = pd.Series([int(a,16) for a in chainw]).diff().dropna()
    hashrate  = pd.Series([(chainwork[a]/1e18)/time_block[a] for a in range(1,len(time_block)+1)])
    hashrate_smoothed = hashrate.rolling(window).median().fillna(np.mean(hashrate[:window]))
    if(hashrate_smoothed.iloc[-1]>aux['hash']):
        alerta(data=hashrate_smoothed.iloc[-1],n=0)
        np.savez('bins/ath.npz',hash=hashrate_smoothed.iloc[-1])
    else: pass
    if(time_block.iloc[-1]>aux['time_total']):
        alerta(n=1,data=time_block.iloc[-1])
        np.savez('bins/ath.npz',time_total=time_block.iloc[-1])
    else: pass
    if(time_block.iloc[-1]>aux['time_halv']):
        alerta(n=2,data=time_block.iloc[-1])
        np.savez('bins/ath.npz',time_halv=time_block.iloc[-1])
    else: pass
    diff = bits_to_difficulty(block['bits'])
    if(diff>aux['dif']):
        alerta(n=3,data=diff)
        np.savez('bins/ath.npz',dif=diff)
    else: pass
    print('Sin cambios en ATH')
    return print('fin analisis bloque nuevo')


#if __name__=='__main__':

    #actualizar(user=rpc_user,passw=rpc_pass)
    #data_metrics()

