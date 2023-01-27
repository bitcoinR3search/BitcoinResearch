import sys, json, requests,time
from time import time
from hashlib import sha256
from urllib.parse import urlparse

def hash_bloque(self):
    bloque_encode = json.dumps(self).encode()
    return sha256(bloque_encode).hexdigest()

class Bloque():
    def __init__(self, indice,hash_anterior,transacciones,tiempo,nonce):
        """ Constructor de la clase bloque.
            indice: indice del bloque.
            transacciones: contendio de transacciones.
            tiempo: Time of generation of the block.
            hash_anterior: la firma del anterior bloque se incluye 
            nonce: el valor que logra cumplir el nuevo hash con la dificultad"""
        self.indice = indice 
        self.hash_anterior = hash_anterior 
        self.transacciones = transacciones 
        self.tiempo = tiempo 
        self.nonce = nonce 

class Blockchain():
    dificultad = '000'

    def __init__(self):
        self.nodes = set()
        self.chain = []
        self.transacciones_pendientes = []
        mensaje_genesis = """genesis_block: 
        este es un mensaje
        que genera el hash 
        que construye al 
        primer bloque"""
        hash_genesis = hash_bloque(mensaje_genesis)
        self.nuevo_bloque(bloque = self.proof_of_work(0,hash_genesis,[],time()))
    
    def proof_of_work(self, indice, hash_anterior,transacciones,tiempo):
        nonce = 0
        bloque = Bloque(len(self.chain),hash_anterior,transacciones,tiempo,nonce)
        while self.validar_pow(bloque.__dict__) is False:
            bloque.nonce += 1
        return bloque

    def validar_pow(self,bloque):
        hash_bloque_nuevo = hash_bloque(bloque)
        return hash_bloque_nuevo[:len(self.dificultad)] == self.dificultad

    def nuevo_bloque(self,bloque):
        self.transacciones_pendientes = []
        self.chain.append(bloque.__dict__)
        return bloque    

    def add_transaction(self, envia, recibe, monto):
        self.transacciones_pendientes.append({
            'monto': monto,
            'recibe': recibe,
            'envia': envia})
        return self.last_block['indice']+1

    @property
    def last_block(self):
        return self.chain[-1]

    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(parsed_url.netloc)

    def update_blockchain(self):
        neighbours = self.nodes
        new_chain = None 
        max_length = len(self.chain)
        for node in neighbours:
            print('http://'+node+'/chain')
            response =requests.get('http://'+node+'/chain')
            if response.status_code == 200:
                length = response.json()['largo']
                chain = response.json()['chain']
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1             
        while current_index < len(chain):
            block = chain[current_index]
            if block['hash_anterior'] != hash_bloque(last_block):
                return False
            if not self.validar_pow(block):
                return False
            last_block = block
            current_index += 1
        return True

