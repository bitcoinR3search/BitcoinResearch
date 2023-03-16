# este script construye un gráfico de la evolución del tamaño de bloques 
# a lo largo del cada bloque


#librerias a usar
import os,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams
import matplotlib.ticker as ticker

fpath = os.path.join(r'bins/MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(48,48,48), (240,240,240), (59,170,6), (61,167,249),(230,0,0)]    

#1[0] fondo plomo
#2    blanco de titulos
#3    rojo neon puntos
#4    verdes
#5    celestes

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
   r, g, b = tableau20[i]    
   tableau20[i] = (r / 255., g / 255., b / 255.)   


# bol = mpimg.imread('bins/logo.jpg')
# imagebox = OffsetImage(bol,zoom=1)
# firma = AnnotationBbox(imagebox)

fig = plt.figure()


#Color del fondo
fig.patch.set_facecolor(tableau20[0])
plt.axes().patch.set_facecolor(tableau20[0])


aux         =  np.load('bins/database.npz', allow_pickle='TRUE') 
n_block     =  aux['n_block']
time_b        =  aux['time_b']
size        =  aux['size']
ntx         =  aux['ntx']
bits        =  aux['bits']
chainwork = aux['chainwork']
strippedsize = aux['strippedsize']
weight = aux['weight']

num_dates = mdates.date2num(time_b)

plt.title('Bitcoin Blockchain \n Block Size History',fontsize=20,fontproperties=prop,color=tableau20[1])
plt.plot(n_block,size/1000,)
#plt.plot(n_block,weight/1000,)
#plt.plot(n_block,strippedsize/1000,)

plt.xlabel('Número de Bloque',fontsize=13,fontproperties=prop,color=tableau20[1])
plt.ylabel('Tamaño en Kbytes',fontsize=13,fontproperties=prop,color=tableau20[1])

plt.xticks(fontsize=10,rotation=45,fontproperties=prop,color=tableau20[1])
plt.yticks(fontsize=10,rotation=45,fontproperties=prop,color=tableau20[1])

plt.xlim(0)
plt.ylim(0,1.2*max(weight/1000))
plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(2,1))
# Ajusta los márgenes de la figura para hacer espacio para el eje x
plt.subplots_adjust(bottom=0.25)
plt.subplots_adjust(top=0.8)
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.text(5000,1800,"Autor: @jpcr3spo Telegram/Twitter",fontsize=5,fontproperties=prop,color=tableau20[2])
plt.savefig('pics/blocksize.png', dpi=300)
plt.close()
