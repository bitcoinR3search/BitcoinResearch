from uuid import uuid4
from core import hash_bloque,Bloque,Blockchain
from time import time
from fastapi import FastAPI
from pydantic import BaseModel

class Transaccion(BaseModel):
    envia: str
    recibe: str
    monto:  float

class Nodo(BaseModel):
    nodes: str

app = FastAPI()
node_identifier = str(uuid4()).replace('-'," ")
blockchain = Blockchain()


@app.get('/chain')
def full_chain():
    resp = {
            'chain': blockchain.chain,
            'largo': len(blockchain.chain)}
    return resp

@app.get('/mine')
def minar_bloque():
    blockchain.add_transaction(monto=50,recibe=node_identifier,envia='coinbase btc')
    hash_bloque_anterior = hash_bloque(blockchain.last_block)
    index = len(blockchain.chain)
    block = blockchain.proof_of_work(index,hash_bloque_anterior,blockchain.transacciones_pendientes,time())
    blockchain.nuevo_bloque(block)
    resp = {
       'mensaje': "Nuevo Bloque Minado!!!",
       'index': block.indice,
       'hash_anterior': block.hash_anterior,
       'nonce': block.nonce,
       'transacciones': block.transacciones}
    return resp

@app.post('/transaciones/new')
async def new_transaction(item: Transaccion):
    blockchain.add_transaction(monto=item.monto,recibe=item.recibe,envia=item.envia)
    resp = {
        'mensaje' : 'Transaccion anadida',
        'Datos' : item.__dict__}
    return resp 

@app.post('/addnode')
async def add_nodes(item: Nodo):
#añade nodos al sistema 
    blockchain.add_node(item.nodes)
    resp = {
        'mensaje': 'Nuevo nodo añadido',
        'nodos en la red': list(blockchain.nodes)}
    return resp

@app.get('/nodo/sync')
def sync():
    updated = blockchain.update_blockchain()
    if updated:
        resp = {
            'mensaje': 'El blockchain se ha actualizado a la cadena mas larga',
            'blockchain': blockchain.chain}
    else:
        resp = {
            'mensaje': 'Su blockchain tiene la cadena más larga',
            'blockchain': blockchain.chain} 
    return resp


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
