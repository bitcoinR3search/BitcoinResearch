from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv
from pprint import pprint
import os

load_dotenv('/home/ghost/.env')


#RPC remote procedure call
rpc_user=  os.getenv('user')
rpc_password=os.getenv('pass')

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@nodeone.local:8332"%(rpc_user, rpc_password))

best = rpc_connection.getblockchaininfo()
pprint(best)


