import hashlib
import json
from datetime import datetime
import random

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = str(datetime.now())
        self.transactions = transactions # Solo una transaccion por bloque 
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
        self.mining_time = None
        self.miner_total_reward = None

    def get_block_data(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        
        
    def serialize_block(self):
        data = self.get_block_data()
        return json.dumps(data, sort_keys=True)


    def compute_hash(self): 
        block_data = self.serialize_block()
        block_string = json.dumps(block_data , sort_keys=True) 
        return hashlib.sha256(block_string.encode()).hexdigest()
    
