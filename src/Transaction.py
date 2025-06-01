import hashlib
from ecdsa import SigningKey, SECP256k1
import json

from UTXO import UTXO


class Transaction:
    def __init__(self, index, sender, receiver, amount, system): 
        self.index = index
        self.sender = sender # ID emisor
        self.receiver = receiver # ID receptor 
        self.amount = amount
        self.system = system
        self.mining_fee = system.mining_fee
        self.total_amount = amount + system.mining_fee
        self.UTXO_set = system.UTXO_set
        # self.receiver_UTXOs = receiver.get_UTXOs()
        if sender is not None:
            self.sender_adress = sender.adress
            self.signing_key = sender.sk
            self.verifying_key = sender.vk
            self.sender_UTXOs = [utxo for utxo in self.UTXO_set if utxo.sender == self.sender_adress]
            self.signature = None
        
        else:
            self.sender_adress = None
            self.signing_key = None
            self.verifying_key = None
            self.sender_UTXOs = []
            self.signature = None

        self.txid = self.create_txid()

        # self.process_transaction()

    def get_transaction_data(self):
        return {
            'index': self.index,
            'sender': self.sender_adress,
            'receiver': self.receiver.adress,
            'amount': self.amount,
            'mining_fee': self.mining_fee,
            'sender_UTXOs': [utxo.serialize_utxo() for utxo in self.sender_UTXOs]
        }

    def serialize_transaction(self):
        data = self.get_transaction_data()
        tx_str = json.dumps(data, sort_keys=True)
        data["txid"] = hashlib.sha256(tx_str.encode()).hexdigest()
        return data

    def create_txid(self):
        tx_str = json.dumps(self.get_transaction_data(), sort_keys=True)
        return hashlib.sha256(tx_str.encode()).hexdigest()
    
    def validate_transaction(self):
        sender_balance = sum(utxo.amount for utxo in self.sender_UTXOs)
        if sender_balance < self.total_amount or self.amount <= 0:
            print("Invalid transaction: insufficient balance or invalid amount")
            return False

        if not self.verify_signature():
            print("Invalid signature")
            return False

        return True

    def sign_transaction(self):
        if self.sender is None:
            return None
        self.signature = self.sender.sign_transaction(self.txid)

    def verify_signature(self):
        if self.signature is None or self.sender is None:
            return True
        return self.sender.verify_signature(self.txid, self.signature.hex())


    def select_utxos(self):
        sender_utxos = sorted(self.sender_UTXOs, key=lambda x: x.amount)
        selected = []
        total = 0

        for utxo in sender_utxos:
            selected.append(utxo)
            total += utxo.amount
            if total >= self.total_amount:
                break

        return selected, total

    
    def process_transaction(self):
        if self.sender is None:
            receiver_utxo = UTXO(self.txid + self.system.get_index_utxo(), self.receiver, self.amount)
            self.UTXO_set.append(receiver_utxo)
            return True
        else: 

            if not self.validate_transaction():
                return False
            self.sign_transaction()
            
            selected_utxos, total_input = self.select_utxos()

            for utxo in selected_utxos:
                self.UTXO_set.remove(utxo)

            new_utxos = []

            receiver_utxo = UTXO(self.txid + self.system.get_index_utxo(), self.receiver, self.amount)
            new_utxos.append(receiver_utxo)


            change = round(total_input - self.total_amount, 1)  # Avoid float issues
            if change > 0:
                change_utxo = UTXO(self.txid + self.system.get_index_utxo(), self.sender, change)
                # change_utxo = UTXO(self.txid, self.sender, change)

                new_utxos.append(change_utxo)
                # self.sender.add_UTXO(change_utxo)


            self.UTXO_set.extend(new_utxos) 
            self.system.mining_fees.append(self.mining_fee)

            return True


        
    
        