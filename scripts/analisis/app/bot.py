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
from readata import time_data, leer_data

#os.chdir('D://proyectos//BitcoinResearch//BitcoinResearch//scripts')
os.chdir('/home/ghost/BitcoinResearch/scripts/')

load_dotenv('bins/.env')

rpc_user = os.getenv('user')
rpc_pass = os.getenv('pass')  


def actualizar_server(user=rpc_user,passw=rpc_pass):
    # este metodo actualiza la db.
    print('Actualizando la DB')
    aux = np.load('bins/database.npz', allow_pickle='TRUE')
    time_b = aux['time_b']
    bits = aux['bits']
    chainwork = aux['chainwork']
    flag = True
    print(f'last block en db {aux["n_block"][-1]}')
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
                print('Actualizando ...')
                #este bucle recopila rapidamente los valores del DB
                print(f'Nuevo bloque encontrado {last_db_block+1}')
                hash = node.getblockhash(last_db_block+1)
                block = node.getblock(hash)
                b, e, f = block['time'], block['bits'], block['chainwork']
                date = datetime.datetime.utcfromtimestamp(b).strftime('%Y-%m-%d %H:%M:%S')
                time_b=np.append(time_b, date)
                bits=np.append(bits, e)
                chainwork=np.append(chainwork, f)
                last_db_block+=1
                last_block = node.getblockcount()
                sleep(1)
            print(f'Actualizado a {last_block}')
            flag=False

        except:
            # si el nodo no esta funcionando espera 
            # 5 minutos antes de volver a intentarlo
            print('error autentificando al nodo')
            print('Probando otra vez en 5 min...')
            sleep(300)
    data_metrics(time_b, bits, chainwork)




def bits_to_difficulty(bits):
        bits = int(bits, 16)
        # Convertir bits a un número de 256 bits en formato big-endian
        target = (bits & 0x007fffff) * 2 ** (8 * ((bits >> 24) - 3))
        # Calcular la dificultad como el cociente entre el objetivo máximo y el objetivo actual
        max_target = 0xffff * 2 ** (8 * (0x1d - 3))
        difficulty = max_target / target
        return difficulty


def data_metrics(time_b,bits,chainw):
    #al llamar a esta función los valores ya estaran actualizados.
    print('Calculando ATH en database')
    difficulty = np.array([bits_to_difficulty(a) for a in bits])
    time_block = pd.Series(pd.to_datetime(time_b)).diff().dt.total_seconds().dropna().replace(0, 1)
    window=1008
    chainwork = pd.Series([int(a,16) for a in chainw]).diff().dropna()
    hashrate  = pd.Series([(chainwork[a]/1e18)/time_block[a] for a in range(1,len(time_block)+1)])
    hashrate_smoothed = hashrate.rolling(window).median().fillna(np.mean(hashrate[:window]))
    hashrate_ath = hashrate_smoothed.max()
    time_ath = time_block.max()
    time_ath_halv = time_block[3*210000:].max()
    dif_ath = difficulty.max()
    np.save('bins/ath_hr.npy',hashrate_ath)
    np.save('bins/ath_tt.npy',time_ath)
    np.save('bins/ath_th.npy',time_ath_halv)
    np.save('bins/ath_d.npy',dif_ath)
    np.save('bins/ath_hrs.npy',hashrate_smoothed[-1008:])
    return print('Guardado en disco')


def alerta(n=0,data=0):
    url = "http://nodetwo.local:8001/notify"
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
            block_anterior_hash = node.getblockhash(block['height']-1)
            block_anterior = node.getblock(block_anterior_hash)
            flag=False
        except:
            # si el nodo no esta funcionando espera 
            # 5 minutos antes de volver a intentarlo
            print('error autentificando al nodo')
            print('Probando otra vez en 5 min...')
            sleep(120)
    aux1 = np.load('bins/ath_hr.npy')
    aux2 = np.load('bins/ath_tt.npy')
    aux3 = np.load('bins/ath_th.npy')
    aux4 = np.load('bins/ath_d.npy')
    aux5 = np.load('bins/ath_hrs.npy')
    print(aux1,aux2,aux3,aux4)
    print('Buscando ATH en bloque...')
    # el primer y mas facil de calcular es el tiempo de llegada
    # para lo cual recuperamos los valores de tiempo
    tiempo_anterior = datetime.datetime.utcfromtimestamp(block_anterior['time']).strftime('%Y-%m-%d %H:%M:%S')
    tiempo_nuevo = datetime.datetime.utcfromtimestamp(block['time']).strftime('%Y-%m-%d %H:%M:%S')
    tiempo_bloque = pd.Series(pd.to_datetime([tiempo_anterior,tiempo_nuevo])).diff().dt.total_seconds().iloc[-1]
    hashrate_new_block = (int(block['chainwork'],16)-int(block_anterior['chainwork'],16))/(1e18*tiempo_bloque)
    print(f'hashrate bloque nuevo {hashrate_new_block}')
    hashrate_mobil = aux5[-1007:]
    #calculamos el hashrate con media movil incluyendo al nuevo dato
    hsrt = np.append(hashrate_mobil,hashrate_new_block)
    hashrate_new_block = hsrt.mean()
    print(f'hashrate promediado {hashrate_new_block}')
    hashrate_mobil = np.append(hashrate_mobil,hashrate_new_block)
    np.save('bins/ath_hrs.npy',hashrate_mobil)
    if(hashrate_new_block>aux1):
        print('Nuevo ATH hashrate')
        alerta(data=hashrate_new_block,n=0)
    else: pass
    if(tiempo_bloque>aux2):
        print('Nuevo ATH total time')
        alerta(n=1,data=tiempo_bloque)
    else: pass
    if(tiempo_bloque>aux3):
        print('Nuevo ATH time halv')
        alerta(n=2,data=tiempo_bloque)
    else: pass
    diff = bits_to_difficulty(block['bits'])
    if(diff>aux4):
        print('Nuevo ATH diff')
        alerta(n=3,data=diff)
    else: pass

    print('Sin cambios en ATH')
    return print('fin analisis bloque nuevo')


if __name__=='__main__':
    actualizar_server(user=rpc_user,passw=rpc_pass)


