class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.UTXO_set = []

    def add_block(self, block):
        self.chain.append(block)
        self.current_transactions = []

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def get_chain(self):
        return self.chain

    def get_current_transactions(self):
        return self.current_transactions
    
