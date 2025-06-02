import hashlib
from ecdsa import SigningKey, SECP256k1
import json

from UTXO import UTXO


class Transaction:
    """
    Represents a transaction within a blockchain system, supporting both standard
    and coinbase transactions.

    A transaction transfers a specified amount of value from a sender to a receiver.
    For regular transactions, the sender must have sufficient unspent transaction outputs (UTXOs).
    Each transaction also includes a mining fee, and produces new UTXOs for the receiver and any change
    to the sender.

    Attributes:
        index (int): Unique identifier for the transaction.
        sender (User or None): The user initiating the transaction. None for coinbase transactions.
        receiver (User): The user receiving the funds.
        amount (float): The amount being transferred to the receiver.
        system (System): Reference to the overarching system to access UTXOs and configuration.
        mining_fee (float): The fixed fee paid to miners.
        total_amount (float): The amount including the mining fee.
        UTXO_set (list): The current set of unspent transaction outputs in the system.
        sender_adress (str or None): The blockchain address of the sender.
        signing_key (SigningKey or None): Sender's private key used for signing.
        verifying_key (VerifyingKey or None): Sender's public key used for verification.
        sender_UTXOs (list): List of UTXOs belonging to the sender.
        signature (str or None): Digital signature of the transaction.
        txid (str): Unique transaction ID derived from transaction data.
    """
    def __init__(self, index, sender, receiver, amount, system): 
        """
        Initializes a transaction object between a sender and receiver.

        Args:
            index (int): Unique transaction index.
            sender (User or None): User initiating the transaction (None for coinbase).
            receiver (User): User receiving the amount.
            amount (float): Amount to transfer (excluding mining fee).
            system (System): Reference to the system to access shared state like UTXO set.
        """
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
        """
        Retrieves structured transaction data for hashing or serialization.

        Returns:
            dict: Dictionary containing index, sender, receiver, amount, mining fee, and sender UTXOs.
        """
        return {
            'index': self.index,
            'sender': self.sender_adress,
            'receiver': self.receiver.adress,
            'amount': self.amount,
            'mining_fee': self.mining_fee,
            'sender_UTXOs': [utxo.serialize_utxo() for utxo in self.sender_UTXOs]
        }

    def serialize_transaction(self):
        """
        Serializes transaction data and adds a transaction ID (txid).

        Returns:
            dict: Serialized transaction dictionary including txid.
        """
        data = self.get_transaction_data()
        tx_str = json.dumps(data, sort_keys=True)
        data["txid"] = hashlib.sha256(tx_str.encode()).hexdigest()
        return data

    def create_txid(self):
        """
        Creates a unique transaction ID by hashing the transaction data.

        Returns:
            str: SHA-256 hash representing the transaction ID.
        """
        tx_str = json.dumps(self.get_transaction_data(), sort_keys=True)
        return hashlib.sha256(tx_str.encode()).hexdigest()
    
    def validate_transaction(self):
        """
        Validates the transaction by checking balance, amount, and digital signature.

        Returns:
            bool: True if the transaction is valid, False otherwise.
        """
        sender_balance = sum(utxo.amount for utxo in self.sender_UTXOs)
        if sender_balance < self.total_amount or self.amount <= 0:
            print("Invalid transaction: insufficient balance or invalid amount")
            return False

        if not self.verify_signature():
            print("Invalid signature")
            return False

        return True

    def sign_transaction(self):
        """
        Signs the transaction ID using the sender’s private key.

        Returns:
            None
        """
        if self.sender is None:
            return None
        self.signature = self.sender.sign_transaction(self.txid)

    def verify_signature(self):
        """
        Verifies the digital signature of the transaction.

        Returns:
            bool: True if the signature is valid or if the transaction is coinbase; False otherwise.
        """
        if self.signature is None or self.sender is None:
            return True
        return self.sender.verify_signature(self.txid, self.signature.hex())


    def select_utxos(self):
        """
        Selects a list of UTXOs from the sender sufficient to cover the transaction total.

        Returns:
            tuple: (list of selected UTXOs, total amount from selected UTXOs)
        """
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
        """
        Processes the transaction by validating, signing, updating the UTXO set,
        and creating new UTXOs for the receiver and sender's change.

        Returns:
            bool: True if the transaction is successfully processed, False otherwise.
        """
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


        
    
        