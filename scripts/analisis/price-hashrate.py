# Importando las bibliotecas necesarias
import yfinance as yf
import pandas as pd

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
from PIL import Image
from app.styles import Estilos, colores
from app.readata import leer_data,time_data
from datetime import datetime


# Definir el ticker para Bitcoin
ticker = 'BTC-USD'
# Crear el objeto de datos
btc_data = yf.download(ticker)

# Extraer las fechas (índice) y el precio de cierre
fecha_p = btc_data.index.strftime('%Y-%m-%d').to_numpy()
precio = np.round(btc_data['Close'].to_numpy(), 2)

chainw, timestamp = leer_data('chainwork','time_b')

# procesamos los datos del tiempo para obtener en segundos 
time = np.array(timestamp, dtype='datetime64[D]')
time_block = pd.Series(pd.to_datetime(timestamp)).diff().dt.total_seconds().dropna().replace(0, 1)

window=4*2016
chainwork = pd.Series([int(a,16) for a in chainw]).diff().dropna()

hashrate  = pd.Series([(chainwork[a]/1e18)/time_block[a] for a in range(1,len(time_block)+1)])
hashrate_smoothed = hashrate.rolling(window).median().fillna(np.mean(hashrate[:window]))

df = pd.DataFrame({
    'date': time[1:],
    'hash_rate': hashrate_smoothed
})

df_grouped = df.groupby('date')['hash_rate'].mean().reset_index()

fecha_hr = df_grouped['date'].to_numpy().astype('datetime64[D]').astype(str)
hashr = df_grouped['hash_rate'].to_numpy()

df_precio = pd.DataFrame({'precio': precio}, index=pd.to_datetime(fecha_p))
df_hash_r = pd.DataFrame({'hash_rate': hashr}, index=pd.to_datetime(fecha_hr))

fecha_inicio = min(df_precio.index.min(), df_hash_r.index.min())
fecha_fin = max(df_precio.index.max(), df_hash_r.index.max())
fechas_completas = pd.date_range(start=fecha_inicio, end=fecha_fin)

df_precio_reindexado = df_precio.reindex(fechas_completas, fill_value=0)
df_hash_r_reindexado = df_hash_r.reindex(fechas_completas, fill_value=hashrate_smoothed.iloc[-1]) # O el valor que consideres lógico

fecha_array = df_precio_reindexado.index.to_numpy()

# Convertir las columnas de precios y hash rate a arrays de NumPy
precio_array = df_precio_reindexado['precio'].to_numpy()
hash_array = df_hash_r_reindexado['hash_rate'].to_numpy()
# Asegurarse de que todas las fechas estén en formato string si es necesario
fecha_array = time_data(fecha_array.astype('datetime64[D]').astype(str))

fpath = os.path.join('bins/MonoLisaSimpson.ttf')
prop = fm.FontProperties(fname=fpath)
fpatht = os.path.join('bins/BigBlueTerm437NerdFont-Regular.ttf')
title = fm.FontProperties(fname=fpatht)
fname = os.path.split(fpath)[1]

tipo='estilo_dark'

fig, ax = plt.subplots(figsize=(18,5), dpi=200)
fig.patch.set_facecolor(Estilos[tipo][1])
ax.patch.set_facecolor(Estilos[tipo][1])

preferencias = {'color':Estilos[tipo][0],'fontproperties':prop}
plt.suptitle("Price and Hashrate\n  Dynamics in Bitcoin",fontsize=45,x=0.3,y=1.45,fontproperties=title,color=Estilos[tipo][0])
 
locator = mdates.MonthLocator(interval=10)
formatter = mdates.DateFormatter('%B\n%Y')
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(labelsize=13, rotation=30,length=5,width=3)
ax.tick_params(axis='both',colors=Estilos[tipo][0])
ax.set_ylabel('Normalized Scale\n', fontsize=18,**preferencias)

# Normalizar precios
precio_min = np.min(precio_array)
precio_max = np.max(precio_array)
precio_n = (precio_array - precio_min) / (precio_max - precio_min)

# Normalizar hash rate
hash_min = np.min(hash_array)
hash_max = np.max(hash_array)
hash_n = (hash_array - hash_min) / (hash_max - hash_min)


ax.plot(fecha_array[360*6:-1],precio_n[360*6:-1],color=colores[3],label='Precio BTC')
ax.plot(fecha_array[360*6:-1],hash_n[360*6:-1],color=colores[5],label='*Hash-Rate')


legend = ax.legend(fontsize=18,loc='center', bbox_to_anchor=(0.12, 1))

legend.get_frame().set_facecolor('#071952')
for text in legend.get_texts():
    text.set_color('w')

date = datetime(2016,6,1)


x_value = mdates.date2num(date)
ax.text(x_value,.8, '*Moving Average\nOver 2016 Blocks',color=Estilos[tipo][0], ha='right', va='center', size=15)



ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for spine in ax.spines.values():
    spine.set_color(Estilos[tipo][0])

indices_cruce = np.where(np.diff(np.sign(precio_n[360*6:] - hash_n[360*6:])))[0]


for i in indices_cruce[-4:]:
    # Usamos i+1 porque el cruce ocurre entre los puntos i y i+1
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='y',s=100) 
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='g',s=30) 
    
for i in indices_cruce[:2]:
    # Usamos i+1 porque el cruce ocurre entre los puntos i y i+1
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='y',s=100) 
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='g',s=30) 

for i in indices_cruce[3:4]:
    # Usamos i+1 porque el cruce ocurre entre los puntos i y i+1
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='y',s=100) 
    ax.scatter(fecha_array[360*6:][i+1], precio_n[360*6:][i+1], color='g',s=30)



date = datetime(2016, 7, 9)
x_value = mdates.date2num(date)
ax.vlines(x_value, 0,.5, colors=Estilos[tipo][0], linestyles='dashed')
date = datetime(2016,5,9)
x_value = mdates.date2num(date)
ax.text(x_value, .5, '2nd\nHalv',color=Estilos[tipo][0], ha='right', va='center', size=13)


date = datetime(2020,5,11)
x_value = mdates.date2num(date)
ax.vlines(x_value, 0,.5, colors=Estilos[tipo][0], linestyles='dashed')
date = datetime(2020,1,11)
x_value = mdates.date2num(date)
ax.text(x_value, .5, '3rd\nHalv',color=Estilos[tipo][0], ha='right', va='center', size=13)

if tipo[7:8] == 'd':
    tw1 = Image.open('bins/br_w.png')
else:
    tw1 = Image.open('bins/br_d.png')
tw1_resized = tw1.resize((int(tw1.width * 0.4), int(tw1.height * 0.4)))
tw1_array = np.array(tw1_resized)
    # Reduce el tamaño de la imagen a la mitad
fig.figimage(tw1_array, xo=2600, yo=1250, alpha=0.55, zorder=1)
plt.savefig('analisis/resultados/priceHash_'+tipo +'.png', bbox_inches='tight', pad_inches=0.75)