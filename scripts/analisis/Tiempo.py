import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from app.styles import Estilos, colores
from app.readata import leer_data
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image


fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

def crear_imagen_total(tipo='estilo_dark'):
	fig, ax = plt.subplots(figsize=(20,5), dpi=200)
	preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
	plt.suptitle("Time\nStamp",fontsize=35,x=0.20,y=1.23,**preferencias)
	time_b = leer_data('time_b')
	
	fig.patch.set_facecolor(Estilos[tipo][1])
	ax.patch.set_facecolor(Estilos[tipo][1])
	#ax.spines.set_color(Estilos[tipo][0])
	fechas=[datetime.strptime(i,"%Y-%m-%d %H:%M:%S") for i in time_b]
	diferencias=[]
	for i in range(1,len(fechas)):
		diferencias.append((fechas[i]-fechas[i-1]).total_seconds())
		
	d=np.array(diferencias)
	d=d/60

	time_b = pd.to_datetime(time_b)
	A_N=[]
	A_N=np.where(d<0,d,0)
	time_b = time_b.date 
	num_dates = mdates.date2num(time_b)


	num_dates=num_dates[:-1]
	######
	locator = mdates.MonthLocator(interval=20)
	formatter = mdates.DateFormatter('%Y-%m')

	#fig, ax = plt.subplots()

	# Configurar los ejes x
	ax.xaxis.set_major_locator(locator)
	ax.xaxis.set_major_formatter(formatter)
	ax.xaxis.set_tick_params(labelsize=10, rotation=20,color='w')
	ax.tick_params(axis='both', labelcolor='w')

	# Dibujar las líneas horizontales
	#ax.axhline(10, color='black')
	#ax.axhline(np.mean(d), color='g')
	#============maximos======
	ax.axvline(num_dates[210000*1], color=Estilos[tipo][0], linestyle='--', linewidth=1)
	#date = datetime(2012,11, 28)
	#x_value = mdates.date2num(date)
	ax.text(num_dates[210000*1],1450,'1st Halving', color=Estilos[tipo][0], ha='right', va='center',size=15)
	##
	ax.axvline(num_dates[210000*2], color=Estilos[tipo][0], linestyle='--', linewidth=1)
	#date = datetime(2016,7, 9)
	#x_value = mdates.date2num(date)
	ax.text(num_dates[210000*2],1450,'2nd Halving', color=Estilos[tipo][0], ha='right', va='center',size=15)
	##
	ax.axvline(num_dates[210000*3], color=Estilos[tipo][0], linestyle='--', linewidth=1)
	#date = datetime(2020,5, 11)
	#x_value = mdates.date2num(date)
	ax.text(num_dates[210000*3],1450,'3rd Halving', color=Estilos[tipo][0], ha='right', va='center',size=15)
	#=====
	indice=np.where((d==np.max(d)))[0][0]
	d_max=d[indice]
	#print(d_max)
	#============minimos=====
	indice2=np.where((d==np.min(d)))[0][0]
	d_min=d[indice2]
	#print(d_min)
	# Dibujar los puntos
	ax.plot(num_dates, d,label="Datos sin anomalias",color=colores[9])

	ax.scatter(num_dates[indice], d_max, color =colores[9],label='Máximo', s=100)
	ax.scatter(num_dates[indice], d_max, color =colores[8],label='Máximo', s=40)
	ax.scatter(num_dates[indice], d_max, color ='r',label='Máximo', s=10)
	

	ax.scatter(num_dates[indice2], d_min, color =colores[7],label='Minimo', s=100)
	ax.scatter(num_dates[indice2], d_min, color =colores[8],label='Minimo', s=40)
	ax.scatter(num_dates[indice2], d_min, color ='red',label='Minimo', s=10)	
	
	#ax.scatter(num_dates[indice2], d_min, color ='red',label='Minimo', s=10)
	#=========anomalias=======
	ax.plot(num_dates[:len(A_N)],A_N,label="Anomalias",color=colores[7])#,s=0.1)

	#Color del fondo dentro la grafica
	
	#fig.set_facecolor('gray')
	tw1 = Image.open('bins/br_w.png')
	tw1_resized = tw1.resize((int(tw1.width * 0.5), int(tw1.height * 0.5)))
	tw1_array = np.array(tw1_resized)
	fig.figimage(tw1_array, xo=2300, yo=850, alpha=0.55, zorder=1)
	plt.subplots_adjust(wspace=0.3, hspace=1)
	#color del fondo
	#ax.patch.set_facecolor('white')
	#===== LEYENDA===
	#scatter.legend_elements(prop="sizes", num=1)[0][0].set_markersize(10)
	#legend_elements=[plt.Line2D([0],[0],marker='o',markersize=10,linewidth=2)]
	#ax.legend(handles=legend_elements)
	###
	ax.set_title("Análisis de los tiempos de llegada de los bloques",loc='left',**preferencias)
	ax.set_xlabel("Fechas de registros",fontsize=17,**preferencias)
	ax.set_ylabel("Diferencias de tiempo [min]",fontsize=17,**preferencias)
	#cuadricula
	ax.grid(axis='y')
	#ax.legend(loc='upper right',title='Leyenda')
	#plt.show()
	#plt.imshow()
	plt.savefig('analisis/resultados/TIEMPO'+tipo+'.png',bbox_inches='tight',pad_inches=0.5)
crear_imagen_total('estilo_dark')