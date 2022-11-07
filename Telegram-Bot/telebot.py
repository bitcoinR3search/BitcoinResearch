#######################################################################
##******************Telegram Nodo Btc********************************##
#######################################################################


# La primera versión solo tiene tres acciones:
# /start - Inicia el bot, realiza un saludo y guarda usuario en log.
# send_ip - manda el ip con que el rpi se conecta.        solo admins
# terminal - Abre una terminal en el rpi por mensajes.    solo admins

# importación de librerias
import json, time, os, sys, logging, telebot
import numpy as np
from telebot import types
from dotenv import load_dotenv


path_assets = '/home/ghost/rpibots/BitcoinResearch/Telegram-Bot/'



########################### ARCHIVOS ########################################
# El bot esta pensado para interactuar con 3 archivos externos:
# 1 El log del bot. Si no existe se crea uno. Este log es para errores o advertencias.
# 2 Usuarios conocidos. Un archivo npy almacena como lista los id de usarios.
# 3 json user : step. Un json que guarda el último lugar del menú donde el user
# se registró. 
# En caso de reinicio o corte abrupto, con estos 3 files se puede recuperar el log de el
# último registro de error y seguir corriendo donde estaba para cada usuario en separado.


# Crea un archivo log si no existe.

if not os.path.exists(path_assets+'bot_telegram.log'):
    with open('bot_telegram.log','w+') as log:
        log.write('#fecha,#hora,#evento,#nivel\n')

#Configurando log del funcionamiento interno del bot. 
logging.basicConfig(filename=path_assets+'bot_telegram.log',filemode='a+',format='%(asctime)s,%(message)s,%(levelname)s', datefmt='%d-%b-%y,%H:%M:%S',level=logging.INFO)
logging.info('Iniciando Bot telegram')
# Cargamos los usuarios conocídos. De no existir creamos una lista vacía.
# KnownUsers es un array de usuarios conocidos

if(os.path.exists(path_assets+'knownUsers.npy')):
    logging.info('Cargando archivo con Usuarios Conocidos')
    aux         = np.load(path_assets+'knownUsers.npy', allow_pickle='TRUE') 
    knownUsers  = aux.tolist()
else:
    logging.info('Creando archivo para nuevos usuarios conocidos')
    knownUsers = []
    np.save(path_assets+'knownUsers.npy',knownUsers)

# Cargamos el archivo json como un diccionario en python. Para transformarlo
# usamos una funcion extra


def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x

if(os.path.exists(path_assets+'userStep.json')):
        logging.info('Cargando json userStep')
        with open(path_assets+'userStep.json','r') as filex:
            userStep=json.load(filex,object_hook=jsonKeys2int) 
else:
    logging.info('Crendo un diccionario userStep')
    userStep = {}  



#####################  Comandos Bot ###############################


#CARGANDO TOKENS
#donde se guardan los tokens como variables de entorno
path = '/home/ghost/rpibots/'
load_dotenv(path+'.env')
# autenrtificación y cuenta maestra
token = os.getenv('token')
master = float(os.getenv('master'))
if token: logging.info('Carde de Credenciales de ingreso ok!')
else: logging.error('Error con carga de Credenciales')

#Comandos del bot

commands = {'start':'Inicia el bot',
            'help'  :'Información del bot',
            'exec'  :'Terminal (Only Admin)'}





#######################################################################
#********************MENU Y RECORRIDO*********************************#
#######################################################################

# El funcionamiento del Bot depende de la ubicacion del usuario dentro de este:
# es como si el bot fuera un lugar (place) con salas que dan acceso a otras salas.

# Por defecto el bot se inicia en el lugar lobby, que espera el comando /start.
# Este comando inicia un registro y saludo al user y lo posiciona en la sala principal.
# es como un  menu = 0 que da acceso a otros dos
# menu = 1 y menu = 2 

menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
menu.add('Send IP')


#######################################################################
#**********************Funciones***************************************#
#######################################################################

#La función get_user_step, se usa para registrar a un nuevo cliente
#y si este existe en el registro, obtener donde se encuentra en el bot
def get_user_step(uid):
    if uid in userStep:      #Busca si existe la llave uid 
        return userStep[uid] #y retorna el valor almacenado de ubicacion 
    else:
        knownUsers.append(uid)   #En caso de no existir el uid registrado 
        userStep[uid] = 0        #se lo almacena y se inicia su ubicacion en cero
        np.save(path_assets+'knownUsers.npy', knownUsers)   #en cada nuevo registro, actualiza.
        logging.info('Nuevo usuario!')
        sv()
        return  userStep[uid]

# actualizar el json con el valor de diccionario
def sv():
    with open(path_assets+'userStep.json','w') as file:
        logging.info('Backup diccionario a Json')
        json.dump(userStep,file)


# La función listener corre cada vez que se invoca al bot
# puede usarse para algún log o para preparar algo previo
def listener(messages):
    for m in messages:
        pass #en este caso no hace nada

#######################################################################
#****************************Inicializamos el bot**********************#
#######################################################################
logging.info('Activando Bot...')
#creamos el objeto Telegram Bot
bot = telebot.TeleBot(token)

if bot:
    logging.info('Bot Listo')
    #asignamos nuestra funcion listener al bot
    bot.set_update_listener(listener)
    sv() #guardamos un backup de userStep (si es nuevo)1
else: logging.error('Error de autentificación!')

#######################################################################
#**********************Estructura de Comandos*************************#
#######################################################################

# START
@bot.message_handler(commands=['start'])
#Cuando se pulse el comando /start
#mira si es un usuario que conoce (en el log) o lo registra si es nuevo
#la variable auxiliar nos ayuda a llevar un orden de menus.
#luego del lobby para usar /start, que seria un valor auxiliar = 0
#viene el menu con dos botones que es como un piso 1, auxiliar = 1 
def command_start(m):
    cid = m.chat.id  # ID del usuario
    if cid in knownUsers:    #Con el ID busca si es conocido.
        #Si es conocido, le envia un saludo
        userStep[cid] = 0
        bot.send_message(cid, "👋Hola,  "+str(m.chat.username)+" que bueno verte nuevamente.",disable_notification= False)
        time.sleep(1)
    else:
        #Si no es conocido, le envia una bienvenida
        bot.send_message(cid, "👋Hola, "+str(m.chat.username)+', ¡Bienvenido!',disable_notification= False)
        time.sleep(1)
        #registra en log 
        bot.send_message(cid, "Te voy registrando...",disable_notification= True)
        get_user_step(cid)
        np.save(path+'knownUsers.npy', knownUsers) 


    bot.send_message(cid, "Iniciando el bot...",disable_notification= True)
    time.sleep(1)
    # Te envia al Menú principal por defecto menu con los botones 
    bot.send_message(cid, "🤖Listo ✅...\nPor favor usa los botones.",reply_markup=menu,disable_notification= False)
    sv()

# AYUDA
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    userStep[cid] = 0
    help_text = "Hola, este bot test\n"
    help_text += "Solo despliega info a un master.\n"
    help_text += "Comandos disponibles: \n"
    bot.send_message(cid, help_text)
    for key in commands:
        help_textk = "/" + key + ": "
        help_textk += commands[key] + "\n"
        bot.send_message(cid, help_textk)
    bot.send_message(cid, "admin site: @jpr3spo",reply_markup=menu) 


# EXEC COMANDO
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    userStep[cid] = 0
    if cid == master:  # cid del admin!
        bot.send_message(cid, "Ejecutan en consola: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        exec_ = os.popen(m.text[len("/exec"):])
        result = exec_.read()
        bot.send_message(cid, "Resultado: " + result,reply_markup=menu)
        logging.info( "Master corrio el comando "+m.text[len('/exec'):])
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo el Admin puede acceder",reply_markup=menu)
        logging.warning( "Alguien no autorizado intenrto usar Terminal!")

#Ahora se configuran los botones del menu 

# solo tiene 'Send IP' y  'Terminal' en un menú

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def menu_menu(m):
    cid = m.chat.id
    text = m.text
    #Una vez en la menu = 0 se delararon 2 opciones:
    if text == 'Send IP':
        if cid == master:
            bot.send_chat_action(cid, 'upload_document')
            mess = 'Se envia en txt la salida del comando ifconfig'
            bot.send_message(cid,mess)
            os.popen('ifconfig > ip.txt')
            time.sleep(2)
            with open('ip.txt','rb') as ips:
                bot.send_document(master,ips,reply_markup=menu)
        #se envia el mensaje y se lo deriva al menu (en el mismo lugar) 
        else: 
            bot.send_message(cid,'onepi.local for not the admin',reply_markup=menu)
            logging.warning('User no autorizado solicito ip')



def menu_loop():
    logging.info('Corriendo el Bot')
    bot.polling(True)


if __name__ == '__menu__':
    #para hacer el bot un poco más robusto 
    #usamos un bucle while y manejo de excepciones  
    logging.info('Iniciando Script Bot Telegram')
    while(1):
        try: #ejecuta la función que corre el bot
            menu_loop()
            #solo con una interrupcion que corta 
            #proceso, manda un mensaje. En otros casos
            #y errores vuelve a ejecutarse.
        except KeyboardInterrupt:
            logging.warning('Salida del Usuario por requerimiento')
            print('\nExiting by user request.\n')
        #lo ideal seria implementar un sistema de logs
        # para otros errores 

