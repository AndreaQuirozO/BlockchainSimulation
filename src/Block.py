import hashlib
import json
from datetime import datetime
import random

class Block:
    """
    A class used to represent a single block in a blockchain.

    Attributes:
        index (int): The position of the block in the blockchain.
        transactions (dict): A dictionary containing the transaction data.
        previous_hash (str): The hash of the previous block in the chain.
        timestamp (str): The timestamp of block creation.
        nonce (int): A number used for mining (proof of work).
        hash (str): The SHA-256 hash of the block's data.
        mining_time (float or None): Time taken to mine the block (optional).
        miner_total_reward (float or None): Total reward earned by the miner (optional).

    Methods:
        get_block_data():
            Returns a dictionary of the block's data (excluding hash).
        
        serialize_block():
            Serializes the block data into a JSON-formatted string.
        
        compute_hash():
            Computes and returns the SHA-256 hash of the serialized block data.
    """
    def __init__(self, index, transactions, previous_hash):
        """
        Initializes a new block.

        Args:
            index (int): The index of the block in the chain.
            transactions (dict): The transaction data contained in the block.
            previous_hash (str): The hash of the previous block in the chain.
        """
        self.index = index
        self.timestamp = str(datetime.now())
        self.transactions = transactions # Solo una transaccion por bloque 
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
        self.mining_time = None
        self.miner_total_reward = None

    def get_block_data(self):
        """
        Retrieves the block's data as a dictionary, excluding the hash.

        Returns:
            dict: A dictionary with the block's index, timestamp, transactions,
                  previous hash, and nonce.
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        
        
    def serialize_block(self):
        """
        Serializes the block's data into a JSON-formatted string.

        Returns:
            str: JSON string of the block data, sorted by keys.
        """
        data = self.get_block_data()
        return json.dumps(data, sort_keys=True)


    def compute_hash(self): 
        """
        Computes the SHA-256 hash of the serialized block data.

        Returns:
            str: The hexadecimal hash of the block.
        """
        block_data = self.serialize_block()
        block_string = json.dumps(block_data , sort_keys=True) 
        return hashlib.sha256(block_string.encode()).hexdigest()
    
