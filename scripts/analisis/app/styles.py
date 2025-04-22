
'''
este script contiene los estilos y colores que se usaran en las gráficas
contiene: 
Colores de la imagen -> estilo_

Colores de los datos -> colores
'''

# se tienen variables que contienen los colores del formato:
# estilo[0]= Titulos y letras 
# estilo[1] = Fondo principal
# estilo[2] = Fondo imagen
estilo_dark=[(255/255., 255/255., 255/255.), (7/255., 25/255., 82/255.), (7/255., 25/255., 82/255.)]
estilo_blanco=[(58/255., 53/255., 59/255.), (255/255., 255/255., 255/255.), (255/255., 255/255., 255/255.)]

Estilos = {
    'estilo_dark': estilo_dark,
    'estilo_blanco': estilo_blanco}

#(255, 219, 225)
# colores: ESTA VARIABLE CONTIENE COLORES
colores = [(255,255,255),         #Blanco     0
            (0,0,0),                #negro      1        La escala de colores primario, fuerte, debil
            (21,150,129),(170, 226, 255),(190, 247, 245), # Verde 2 3 4  
            (255, 3, 45),(79, 32, 40),(255, 192, 203),   # Rojo 5 6 7 
            (7,25,82), #AZUL DE FONDO
            (170, 226, 255,),#CELESTE DE LINEA
            (0, 128, 255)   #AZUl marino
            ]




#transforma la lista ed colores en RGB float
colores=[(r / 255., g / 255., b / 255.) for r,g,b in colores]

