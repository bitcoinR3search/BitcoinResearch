
#librerias 

#usar comandos del sistema
import os
#manejo numerico
import numpy as np
#graficar
import matplotlib.pyplot as plt
#libreria manejo de tipografia
from matplotlib import font_manager as fm, rcParams

#cambiar la typografia
fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]



#tabla de colores
tabla_color = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
    (44, 44, 44),] 

#tabla_color[0] = plomo , para el fondo.
#tabla_color[1] = plomo+morado, para el fondo 
#tabla_color[2] = blanco, para las letras

#tabla_color[3] = naranja, para la curva 







for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   



fig, ax = plt.subplots()


#titulo
plt.title(r"$\bf{BITCOIN:\ HISTORIAL\ DEL\ NÚMERO\ DE\ TX}$" "\n" r"$\it{Comparación\ por\ bloque\ y\ por\ acumulado}$",fontsize=10,color=tableau20[8],fontproperties=prop)


#Color del fondo
fig.patch.set_facecolor(tableau20[4])
plt.axes().patch.set_facecolor(tableau20[5])




t=np.linspace(0,13,20)
xt=np.sin(t)
plt.scatter(t,xt,label="disperso",color=tableau20[3])


plt.savefig('test.png')