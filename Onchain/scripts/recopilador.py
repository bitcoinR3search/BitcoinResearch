# Este script es un ejemplo de como se puede
# recopilar data del bitcoin usando el nodo

# librerias

#coneccion con el nodo
from bitcoin.rpc import RawProxy
#para enmascarar tokens
from dotenv import load_dotenv
#diversos
import os, datetime, time, logging, sys
import numpy as np
#ver el estado de un proceso
from tqdm import tqdm


# cargamos variables de autentificacion
load_dotenv('.env')
rpc_user=  os.getenv('user')
rpc_password=os.getenv('pass')

# iniciamos logs 
logging.basicConfig(filename='bins/recopilador.log',filemode='a+',format='%(asctime)s,%(message)s,%(levelname)s', datefmt='%d-%b-%y,%H:%M:%S',level=logging.INFO)
logging.info('*****************START***************************')
logging.info('Corriendo script '+f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# autentificación

try:
   node = RawProxy(service_url='http://%s:%s@nodeone.local:8332'%(rpc_user, rpc_password))
   #si todo esta ok y el nodo esta online acepta sesion
   logging.info('Autentificando sesion')
except:
   #si el nodo esta offline o no se logra autentificar
   logging.info('Error de auth sesion')
   logging.info('Cerrando Todo')
   logging.info('********************************************')
   #directamente sale al sistema
   sys.exit()
   
# Este script reconoce si existen los binarios y base de datos. 
# de no ser asi, empieza creandolos.

if(os.path.exists('bins/database.npz')):
   logging.info('Se detecto la db en bins/database.npz')
   aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
   n_block     =  aux['n_block']
   time_b        =  aux['time_b']
   size        =  aux['size']
   ntx         =  aux['ntx']
   bits        =  aux['bits']
   chainwork = aux['chainwork']
   strippedsize = aux['strippedsize']
   weight = aux['weight']



else:
   logging.info('No existe la db, creando variables')
   n_block = np.array([])
   time_b = np.array([])
   size = np.array([])
   ntx = np.array([])
   bits = np.array([])
   chainwork = np.array([])
   strippedsize = np.array([])
   weight = np.array([])
# blockchain dividimos por lotes.
# se podria ejecutar en cualqueir momento, verifica y reconoce el último dato 
# introducido y sigue desde este punto para adelante.



# Recoge el valor de altura de bloque ya recopilada
if any(n_block):
   last = n_block[-1]
   logging.info('ultimo bloque en db %d',last)
else: 
   last = 1
   logging.info('Iniciando con el bloque 1')


lote = 100000 # en nuestro caso procesaremos lotes de 5000 bloques
N_MAX = 800000 # El script prevee un tope arbitrario (mayor al último bloque)

nn = N_MAX//lote # calcula el numero entero de cuantas vueltas
#necesita para recorrer todo el blockchain

print('LOTES de %d bloques: %d'%(lote,nn))

# encontramos el indice de lote donde corresponde la busqueda
if last<lote:
   a = 1
else:
   a = (last)//lote

flag=True
while(flag):
   try:
      #debe realizar el recorrido hasta el último bloque.
      n_max =  node.getblockcount()
      flag = False
   except:
      time.sleep(3)


for ix in range(int(a),int(nn)+1): 
   print('-> lote: ',ix)

   if ix==nn:
      stop = n_max
   else:
      stop = ix*lote

   
   for n in tqdm(range(int(last),stop+1),desc ="Recopilando lote: %d"%ix):
   #ahora que tenemos el puntero en el bloque correcto empezamos a hacer calls al nodo
   #lo q puede fallar por algún x motivo. De ser así vuelve a ejecutar el call 3 seg despúes.
      flag=True   
      while(flag):
         try:
            hash = node.getblockhash(n)
            logging.info('nuevo bloque %d',n)
            block = node.getblock(hash)
            a,b,c,d,e,f,g,h = block['height'],block['time'],block['size'],block['nTx'],block['bits'],block['chainwork'],block['strippedsize'],block['weight']
            n_block=np.append(n_block,a)
            date=datetime.datetime.utcfromtimestamp(b).strftime('%Y-%m-%d %H:%M:%S')
            time_b=np.append(time_b,date)
            size=np.append(size,c)
            ntx=np.append(ntx,d)
            bits=np.append(bits,e)
            chainwork = np.append(chainwork,f)
            strippedsize = np.append(strippedsize,g)
            weight = np.append(weight,h)
            flag=False
         except:
            time.sleep(3)
   last=stop+1
   print('LOTE TERMINADO: ',ix)
   np.savez('bins/database.npz', n_block=n_block, date=date,time_b=time_b,size=size,ntx=ntx,bits=bits,chainwork=chainwork,strippedsize=strippedsize,weight=weight)
   logging.info('Guardando db lote: %d',ix)

logging.info('******************EXIT**************************')