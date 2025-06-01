from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, BadSignatureError

class User:
    def __init__(self, index):
        self.index = index
        self.private_key, self.public_key = self.create_keys()
        self.adress = self.create_adress()


    def create_keys(self):
        self.sk = SigningKey.generate(SECP256k1, hashfunc=sha256)
        self.vk = self.sk.verifying_key
        private_key = self.sk.to_string().hex()
        public_key = self.vk.to_string().hex()
        return private_key, public_key
    

    def create_adress(self):
        return sha256(self.public_key.encode()).hexdigest()
    
    
    def get_balance(self, UTXO_set):
        return sum(utxo.amount for utxo in UTXO_set if utxo.sender == self.adress)


    def sign_transaction(self, message):
        return self.sk.sign(message.encode(), hashfunc=sha256)
    
    def verify_signature(self, message, signature):
        try:
            return self.vk.verify(bytes.fromhex(signature), message.encode())
        except BadSignatureError:
            return False
    
    
    # def select_utxos(self, UTXO_set, total_amount):
    #     users_utxos = [utxo for utxo in UTXO_set if utxo.sender == self.adress]
    #     sender_utxos = sorted(users_utxos, key=lambda x: x.amount)
    #     selected = []
    #     total = 0

    #     for utxo in sender_utxos:
    #         selected.append(utxo)
    #         total += utxo.amount
    #         if total >= self.total_amount:
    #             break

    #     return selected, total

