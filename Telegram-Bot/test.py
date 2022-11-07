import logging



# with open('bot_telegram_log_sistem.log','w+') as log:
#    log.write('#fecha,#hora,#evento,#nivel\n')


logging.basicConfig(filename='bot_telegram_log_sistem.log',filemode='a+',format='%(asctime)s,%(message)s,%(levelname)s', datefmt='%d-%b-%y,%H:%M:%S',level=logging.INFO)




a = 3

if a>2:
   logging.info('Admin logged inbbout')
else:
   logging.info('Admin logged out')

