# Este script es un ejemplo de como se puede
# recopilar data del bitcoin usando el nodo


from bitcoin.rpc import RawProxy
from dotenv import load_dotenv
import os, datetime, time, logging, sys
import numpy as np


# cargamos variables de autentificacion
load_dotenv('.env')
rpc_user=  os.getenv('user')
rpc_password=os.getenv('pass')


logging.basicConfig(filename='bins/recopilador.log',filemode='a+',format='%(asctime)s,%(message)s,%(levelname)s', datefmt='%d-%b-%y,%H:%M:%S',level=logging.INFO)
logging.info('********************************************')
logging.info('Corriendo script '+f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# autentificación

try:
   node = RawProxy(service_url='http://%s:%s@nodeone.local:8332'%(rpc_user, rpc_password))
   logging.info('Autentificando sesion')
except:
   logging.info('Error de auth sesion')
   logging.info('Cerrando Todo')
   logging.info('********************************************')
   sys.exit()
   
# creamos las variables a usar si es que no existen

if(os.path.exists('bins/database.npz')):
   logging.info('Se detecto la db')
   aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
   n_block     =  aux['n_block']
   time        =  aux['time']
   size        =  aux['size']
   ntx         =  aux['ntx']
else:
   logging.info('No existe la db')
   n_block  =  np.array([])
   time     =  np.array([])
   size     =  np.array([])
   ntx      =  np.array([])

# para poder procesar todo el blockchain dividimos por lotes
# de manera que pueda reconocer el último dato introducido y seguir 
# desde ese punto

# puede ser que sea el primer avance, entonces 
if any(n_block):
   last = int(n_block[-1])
   logging.info('ultimo bloque %d',last)
else: 
   last = -1
   logging.info('Iniciando con bloque gen')

lote = 50000 # cada 10 bloques, de funcionar se sube

for n in range(last+1,last+lote+1):
   #evitamos que un rango sea mayor al bloque mas alto   
   #de igual manera puede ser que una llamada al bitcoin-cli
   #genere un error.
   while(True):
      try:
         n_max =  node.getblockcount()
         if n <= n_max:
            logging.info('nuevo bloque %d',n)
            hash = node.getblockhash(n)
            block = node.getblock(hash)
            a,b,c,d=block['height'],block['time'],block['size'],block['nTx']
            n_block=np.append(n_block,a)
            date=datetime.datetime.utcfromtimestamp(b).strftime('%Y-%m-%d %H:%M:%S')
            time=np.append(time,date)
            size=np.append(size,c)
            ntx=np.append(ntx,d)
            logging.info('datos guardados de %d',n)
            break
         else: break
      except:
         time.sleep(3)

np.savez('bins/database.npz', n_block=n_block, date=date,time=time,size=size,ntx=ntx)
logging.info('Guardando db')
logging.info('********************************************')
   