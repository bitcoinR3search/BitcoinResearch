from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user='ghost'
rpc_password='2453889Crespo'
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))

best = rpc_connection.getblockchaininfo()
print(best['verificationprogress'])

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
