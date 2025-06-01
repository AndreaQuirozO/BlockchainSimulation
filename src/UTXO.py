import json
import hashlib

class UTXO:
    def __init__(self, utxo_id, user, amount):
        self.utxo_id = utxo_id
        self.sender = user.adress
        self.amount = amount

    def serialize_utxo(self):
        utxo_data = {
            'utxo_id': self.utxo_id,
            'sender': self.sender,
            'amount': self.amount
        }
        return json.dumps(utxo_data, sort_keys=True)
