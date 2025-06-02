import json
import hashlib

class UTXO:
    """
    Represents an Unspent Transaction Output (UTXO) in the blockchain system.

    Each UTXO records a certain amount of cryptocurrency that can be used as input for future transactions.
    UTXOs are associated with a user's address and are uniquely identified.

    Attributes:
        utxo_id (str): Unique identifier of the UTXO, typically derived from the transaction.
        sender (str): Address of the user who owns this UTXO.
        amount (float): Value of the UTXO available for spending.
    """
    def __init__(self, utxo_id, user, amount):
        """
        Initializes a new UTXO instance with a unique ID, owner, and amount.

        Args:
            utxo_id (str): Unique identifier for the UTXO.
            user (User): The user object who owns the UTXO.
            amount (float): The amount of cryptocurrency associated with this UTXO.
        """
        self.utxo_id = utxo_id
        self.sender = user.adress
        self.amount = amount

    def serialize_utxo(self):
        """
        Serializes the UTXO data into a JSON-formatted string.

        Returns:
            str: A JSON string representing the UTXO, with keys sorted alphabetically.
        """
        utxo_data = {
            'utxo_id': self.utxo_id,
            'sender': self.sender,
            'amount': self.amount
        }
        return json.dumps(utxo_data, sort_keys=True)
