#######################################################################
#********Script Bot Telegram Nodo Btc*********************************#
#######################################################################


# importación de librerias
import telebot, json, time, os, sys
import numpy as np 
from telebot import types
from dotenv import load_dotenv

path = '/home/ghost/Desktop/proyectos/bots/bitbolnode/bins/' #ruta del archivo log

# Cargamos base de datos 
data = np.load(path+'bd_tb.npy',allow_pickle=True)
fibu = np.load(path+'fibu.npy',allow_pickle=True)

# Las variables de autentificación se cargan como variables de entorno
load_dotenv('/home/ghost/Desktop/proyectos/.env')

# autenrtificación y cuenta maestra
token = os.getenv('token')
master = float(os.getenv('master'))

#comandos que ingresas al bot ej /start

commands = {'start'  :   'Inicia el bot',
             'help'     :  'Como funciona el Bot',
             'nodoinfo' :   'Informacion del Nodo (only master)',}


#El manejo y gestión del bot para cada usuario es distinto.
#para evitar que el usario se quede en un bucle guardamos 
#el usuario y su ubicación en el recorrdo del bot


# Cargamos los usuarios conocídos. De no existir creamos una lista vacía.
# KnownUsers es un array de usuarios conocidos

if(os.path.exists(path+'knownUsers.npy')):
	aux         = np.load(path+'knownUsers.npy', allow_pickle='TRUE') 
	knownUsers  = aux.tolist()
else:
    knownUsers = []
    np.save(path+'knownUsers.npy',knownUsers)

#########FUNCIONES ESPECIALES #########################################

# para leer json y transformarla a diccionario python
def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x


#Función guardar el estado de la ubicación del usuario.
def sv():
    with open(path+'userStep.json', 'w') as file:
        #el valor de ubicacion se guarda en el archivo json
        json.dump(userStep,file)

#######################################################################

#Cargamos el último lugar donde se registro el usuario 
# userStep es un diccionario (clave|valor -> usuario|ubicacion)
if(os.path.exists(path+'userStep.json')):
    with open(path+'userStep.json','r') as filex:
        userStep=json.load(filex,object_hook=jsonKeys2int) 
else:
    userStep = {}  
    sv()

#######################################################################
#********************MENU Y RECORRIDO*********************************#
#######################################################################

# El funcionamiento del Bot depende de la ubicacion del usuario dentro de este:
# es como si el bot fuera un lugar (place) con salas que dan acceso a otras salas.

# Por defecto el bot se inicia en el lugar lobby, que espera el comando /start.
# Este comando inicia un registro y saludo al user y lo posiciona en la sala principal.
# es como un  menu = 0 que da acceso a otros dos
# menu = 1 y menu = 2 

menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
menu.add('Bot 🤖 Tools','RaspberryPi-Node Info')

# El menu de Inicio menu = 1 que da acceso a (en orden)
# menu = 3   menu = 4 y menu = 0 (atrás)

in_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
in_menu.add('Info 👁️ solo 🇧🇴 🔎','BTC TOOLS','🔙Atrás')

## date 02/08/2022:
# Info Solo te lleva a un menu de busqueda
# BTC Tools esta en construcción por lo que solo despliega un mensaje


# El menu de datos Bolivia tiene el comando para la busqueda y atrás. Fin del camino.
bo_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
bo_menu.add('Realiza una busqueda','🔙Atrás')




# El menu de RpiInfo menu = 2 que da acceso a comandos TEMP RAM CPU
# y permite volver a menu = 0 

nodo_menu = types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True,one_time_keyboard=False)
nodo_menu.add('Temperatura','Ram','CPU','IP rout (master)','🔙Atrás')




#######################################################################
#**********************Funciones***************************************#
#######################################################################


# Función para obtener la ubicación en el bot del usuario

def get_user_step(uid):
       if uid in userStep:      #Busca si existe la llave uid
           return userStep[uid] #y retorna el valor almacenado de ubicacion
       else:
           knownUsers.append(uid)   #En caso de no existir el uid registrado
           userStep[uid] = 0        #se lo almacena y se inicia su ubicacion en cero
           #retorna el valor de ubicacion
           return  userStep[uid]



# Función para registrar un log

#simplemente un conteo de usos de funciones. Para mejorar el desarrollo futuro.  
def listener(messages):
    for m in messages:
        with open(path_log+'log_telegrambot.txt', 'a') as _log:
            _log.write(str(m.chat.id)+'->'+str(m.chat.username)+':'+str(get_user_step(m.chat.id))+'\n')

#######################################################################
#****************************Inicializamos el bot**********************#
#######################################################################

#creamos el objeto Telegram Bot
bot = telebot.TeleBot(token)
#asignamos nuestra funcion listener al bot
bot.set_update_listener(listener)

#######################################################################
#**********************Estructura de Comandos*************************#
#######################################################################

# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id  # ID del usuario
    if cid in knownUsers:    #Con el ID busca si es conocido.
        #Si es conocido, le envia un saludo y resetea su lugar a cero
        userStep[cid] = 0
        bot.send_message(cid, "👋Hola,  "+str(m.chat.username)+" que bueno verte nuevamente.",disable_notification= False)
        time.sleep(1)
    else:
        #Si no es conocido, le envia una bienvenida
        bot.send_message(cid, "👋Hola, "+str(m.chat.username)+', ¡Bienvenido!',disable_notification= False)
        time.sleep(1)
        bot.send_message(cid, "Te voy registrando...",disable_notification= True)
        get_user_step(cid); #en esta llamada siempre se registra el usuario con ubicacion menu = 0
        np.save(path+'knownUsers.npy', knownUsers) 


    bot.send_message(cid, "Iniciando el bot...",disable_notification= True)
    time.sleep(1)
    # Te envia al Menú principal por defecto menu = 0. 
    bot.send_message(cid, "🤖Listo ✅...\nPor favor usa los botones.",reply_markup=menu,disable_notification= False)
    sv() #guardamos el estado de la ubicacion de los usuarios en menu = 0. Nuevos o conocidos q usen /start

# AYUDA
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    #suponemos que el usuario ya esta registrado antes de poder usar el comando /help
    #pq necesitas usar el comando /start al inicio de todo bot.
    userStep[cid] = 0 
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    help_text = '''Este Bot 🤖 es una herramienta que esta implementada sobre el Nodo Bitcoin BitBol.
Toda información es verificada y validada por el mismo nodo, así como el procesamiento de cada solicitud de información.
Se pueden usar los siguientes comandos:'''
    bot.send_message(cid, help_text,reply_markup=menu,disable_notification= True)
    for key in commands:
        help_textk = "/" + key + ": "
        help_textk += commands[key] + "\n"
        bot.send_message(cid, help_textk,reply_markup=menu,disable_notification= True)
    sv() #guardamos el estado de la ubicacion de los usuarios en menu = 0. Help no tiene mas función.
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    about='''Este bot fue construido por Industrias Bot 💪💻 puede contactarse en el siguiente enlace: 
    📲 https://t.me/jpcr3spo\n
    👨‍💻 El repositorio del proyecto se encuentra en: 
    🌐 https://github.com/jpcrespo/bitbolnode\n

    La base de datos de los números de Bolivia filtrados en Facebook fue gracias a: 
    🐦 https://twitter.com/ccuencad'
    un agradecimiento especial.''' 
    bot.send_message(cid,about,disable_web_page_preview=True)
    bot.send_message(cid,'Menú principal:',reply_markup=menu,disable_notification= True)

# Info Nodo
@bot.message_handler(commands=['nodoinfo'])
def command_exec(m):
    cid = m.chat.id
    userStep[cid] = 0
    if cid == master:  # cid del admin!
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "Acceso TOR remoto: ")
        time.sleep(1)
        bot.send_message(cid,"6zhd7yhn5ntoemfc2qkgezl4gefg7ou5csfczzs4sl6ewwqonwvapvyd.onion",reply_markup=menu,disable_notification= True)
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo el Admin del Nodo puede acceder",reply_markup=menu,disable_notification= True)
    sv() #guardamos el estado de la ubicacion de los usuarios en menu = 0. Info Nodo no tiene mas función.



#######################################################################
#Para gestionar el recorrido del usuario, usamos el get_user_step 
#y ponemos los servicios en cada sala menu que se declaro en MENY Y RECORRIDO
#######################################################################

# menu = 0 
# cuando el usuario da /start se despliega el menu principal que da acceso
# a los otros menus. 

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def menu_menu(m):
    cid = m.chat.id
    text = m.text
    #Una vez en la menu = 0 se delararon 2 opciones:
    if text == "Bot 🤖 Tools":
        userStep[cid] = 1
        bot.send_chat_action(cid, 'typing')
        mess = '''Este bot tiene herramientas para responder bajo consulta, la verificación de información de la Red Bitcoin.
        Por favor selecciona una opción:'''
        #se envia el mensaje y se lo deriva al menu = 1 
        bot.send_message(cid,mess,reply_markup=in_menu)
    elif text == 'RaspberryPi-Node Info':
        userStep[cid] = 2
        mess = '''Se brinda información sobre el Nodo BitBol, que corre en un RaspberryPi4. Muestra algunas variables del sistema como la temperatura del CPU, la memoria libre, etc.'''
        #se envia el mensaje y se lo deriva al menu = 2
        bot.send_message(cid,mess,reply_markup=nodo_menu)

# menu = 1
# En este momento el usuario tiene el menu in_menu
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def rpi_info(m):
    cid = m.chat.id
    if m.text == "Info 👁️ solo 🇧🇴 🔎":
    #se queda en este lugar el bucle hasta q decida salir con atras
        userStep[cid] = 3
        bot.send_chat_action(cid, 'typing')
        mess = '''En febrero de 2021 se hizo pública una base de datos robada a Facebook.

        https://www.businessinsider.com/stolen-data-of-533-million-facebook-users-leaked-online-2021-4 

        👁️ «El robo afecto a cuentas sin importar si se configuraron con privacidad para no mostrar esta información».

        Se afectaron más de 3 millones de cuentas de Bolivia 🇧🇴 asociadas a un número celular (de cualquier empresa: Entel, Tigo, Viva). Estas son usadas por los estafadores junto a la información que se puede obtener del mismo perfil de Facebook, como el nombre, la edad, el sexo, estado, etc.

        Esta Herramienta le permite consultar si su número de celular se encuentra en la filtración. De estarlo se aconseja cambiar de número o cerrar/cambiar el perfil de facebook asociado.'''
        bot.send_message(cid, mess,disable_web_page_preview=False,disable_notification=False,reply_markup=bo_menu)


    elif m.text == 'BTC TOOLS':
        userStep[cid] = 1
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "EN CONSTRUCCION",reply_markup=in_menu)

    elif m.text == '🔙Atrás':
        userStep[cid] = 0
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "Menú principal:",reply_markup=menu)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def leak(m):
    cid = m.chat.id
    if m.text == 'Realiza una busqueda':
        userStep[cid] =3
        markup = types.ForceReply(selective=False)
        target_n =  bot.send_message(cid,"Ingrese su número 591: ",reply_markup=markup);
        bot.register_next_step_handler(target_n,busqueda)
    elif m.text == '🔙Atrás':
        userStep[cid] = 0
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "Menú principal:",reply_markup=menu)

#****************** busqueda del número en filtración *************************

def busqueda(m):
    cid=m.chat.id
    nn=m.text
    if nn.isdigit():
        n1=int(nn)
        n2=59100000000+n1
        _a=np.where(data == n2)
        if(n1>60000000 and n1<79999999):
            bot.send_message(cid,"Revisando en la base . . .🔍️🔍️🔍️")
            if (len(_a[0])==0):
                bot.send_chat_action(cid, 'typing')
                time.sleep(1)
                bot.send_message(cid,"Su número no esta en la filtración ✔️",reply_markup=bo_menu)
            else:
                bot.send_message(cid,"Su número ESTA en la filtración, tenga cuidado ⚠️")
                bot.send_message(cid,"Facebook asociado: https://facebook.com/"+str(fibu[_a[0][0]]),reply_markup=bo_menu)
            
        else:
            bot.send_message(cid,"No es un número de Bolivia o esta mal escrito.",reply_markup=bo_menu)
    
    else:
        bot.send_message(cid,"Dato introducido no válido",reply_markup=bo_menu)




# MENU PRINCIPAL










def menu_loop():
    print('Corriendo...')
    bot.polling(True)


if __name__ == '__menu__':
    

        try:
                menu_loop()
        except KeyboardInterrupt:
                print('\nExiting by user request.\n')
