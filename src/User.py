from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, BadSignatureError

class User:
    """
    Represents a user in the blockchain system with a cryptographic key pair and unique address.

    Each user has a public-private key pair used to sign and verify transactions.
    The address is derived from the user's public key and serves as their identifier on the blockchain.

    Attributes:
        index (int): Unique ID for the user.
        sk (SigningKey): ECDSA private key for signing messages.
        vk (VerifyingKey): ECDSA public key for verifying signatures.
        private_key (str): Hex representation of the private key.
        public_key (str): Hex representation of the public key.
        adress (str): SHA-256 hash of the public key, used as the user’s blockchain address.
    """
    def __init__(self, index):
        """
        Initializes a new user with a unique index, key pair, and blockchain address.

        Args:
            index (int): The unique identifier of the user.
        """
        self.index = index
        self.private_key, self.public_key = self.create_keys()
        self.adress = self.create_adress()


    def create_keys(self):
        """
        Generates an ECDSA key pair (SECP256k1) for the user.

        Returns:
            tuple: (private_key (str), public_key (str)) in hexadecimal format.
        """
        self.sk = SigningKey.generate(SECP256k1, hashfunc=sha256)
        self.vk = self.sk.verifying_key
        private_key = self.sk.to_string().hex()
        public_key = self.vk.to_string().hex()
        return private_key, public_key
    

    def create_adress(self):
        """
        Creates a blockchain address by hashing the public key with SHA-256.

        Returns:
            str: Hexadecimal SHA-256 hash of the public key.
        """
        return sha256(self.public_key.encode()).hexdigest()
    
    
    def get_balance(self, UTXO_set):
        """
        Calculates the total balance available to the user based on the current UTXO set.

        Args:
            UTXO_set (list): List of all unspent transaction outputs in the system.

        Returns:
            float: Sum of amounts for UTXOs associated with this user's address.
        """
        return sum(utxo.amount for utxo in UTXO_set if utxo.sender == self.adress)


    def sign_transaction(self, message):
        """
        Signs a message using the user's private key.

        Args:
            message (str): The message to be signed.

        Returns:
            bytes: The digital signature.
        """
        return self.sk.sign(message.encode(), hashfunc=sha256)
    
    def verify_signature(self, message, signature):
        """
        Verifies the digital signature of a message using the user's public key.

        Args:
            message (str): The original message.
            signature (str): The hexadecimal representation of the signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        try:
            return self.vk.verify(bytes.fromhex(signature), message.encode())
        except BadSignatureError:
            return False
    
    

