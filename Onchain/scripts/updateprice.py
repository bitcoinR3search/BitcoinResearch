# En este script vemos como usar un request
# a una url que devuelve datos en json

import json, requests, datetime
import sys

sys.stdout = open('bins/pricebtc.txt', 'a')

def func():
   now = datetime.datetime.now()

   url_req = requests.get('http://api.coindesk.com/v1/bpi/currentprice.json')
   data = url_req.json()['bpi']['USD']['rate']
   data_clean = float(data.replace(',', ''))
   print(round(data_clean,2),end=' ')
   print('USD',end=',')
   print(now.strftime("%Y-%m-%d %H:%M:%S"))


if __name__== "__main__":
   func()

sys.stdout.close()