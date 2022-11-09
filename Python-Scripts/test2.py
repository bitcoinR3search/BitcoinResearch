from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user='raspibolt'
rpc_password='2453889'
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
best_block_hash = rpc_connection.getblockchaininfo()
print(best_block_hash)

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
