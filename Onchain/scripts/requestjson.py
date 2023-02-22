# En este script vemos como usar un request
# a una url que devuelve datos en json

import json, requests
from pprint import pprint

# direction = '1Cdid9KFAaatwczBwBttQcwXYCpvK8h7FK'
# url_req = requests.get('https://blockchain.info/unspent?active='+direction)
# datos = url_req.json()


url_req = requests.get('http://api.coindesk.com/v1/bpi/currentprice.json')
data = url_req.json()['bpi']['USD']['rate']
data_clean = float(data.replace(',', ''))
print(round(data_clean,2))