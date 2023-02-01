#from dotenv import load_dotenv
from bitcoin.rpc import RawProxy
from pprint import pprint
from dotenv import load_dotenv

import os 


load_dotenv('test/.env')


#RPC remote procedure call
rpc_user=  os.getenv('user')
rpc_password=os.getenv('pass')
p = RawProxy(service_url='http://%s:%s@nodebtc.local:8332'%(rpc_user, rpc_password))

info = p.getblockchaininfo()

pprint(info)



