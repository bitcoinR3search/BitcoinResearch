# Este script calcula la cantidad de Bitcoin (en satoshis) que se va a emitir


# La función trunc nos retorna la parte entera de un número.
# Se calcula la recompensa en sats y se toma su valor entero
# puesto que es la unidad mínima y no se puede redondear. 

import matplotlib.pyplot as plt
from matplotlib import style
from math import trunc
#la recompensa inicial son 50*10^8 sats (50 btc)
recompensa = 50 * 10**8
#un halv ocurre cada 210000 bloques
limite = 210000

btc = 0
halv = 0
blocks = 0
year = 2009

## para graficar

# x representa los bloques
x = [0,]
# y representa btc emitido
y = [0,]
# un y1 para normalizar y sacar porcentajes
y1=[]



while(recompensa > 0):
   for i in range(0,limite):
      btc+=recompensa
      blocks+=1
   print('Halv: ',halv,end=' | ')
   print('Recompensa (sats): ',recompensa,end=' | ')
   print('Bitcoin emitido (btc): ',btc/10**8,end=' | ')
   print('Bloques emitidos: ',blocks,end=' | ')
   print('Año: '+str(year)+'-'+str(year+3) )
   recompensa=trunc(recompensa/2)
   year += 4
   halv += 1 
   x.append(halv)
   y.append(btc/10**8)

print('btc total a emitir: ',btc/10**8)



plt.style.use('dark_background')
plt.title('\nEmision Total Btc: '+str(y[-1])+'\n')
for i in y:
   y1.append(100*i/(btc/10**8))
	

plt.plot(x[:9],y1[:9])
plt.xlabel('Halving')
plt.xticks(x[:9])
plt.ylabel('% de btc emitido')
plt.yticks(y1[:5])
plt.grid()
plt.show()



