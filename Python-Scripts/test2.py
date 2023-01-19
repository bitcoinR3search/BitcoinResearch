from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user='ghost'
rpc_password='2453889Crespo'
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@192.168.1.6:8332"%(rpc_user, rpc_password))

best = rpc_connection.getblockchaininfo()
print(best['verificationprogress'])


