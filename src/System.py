import random
import time

from User import User
from Transaction import Transaction
from UTXO import UTXO
from Block import Block


class System:
    def __init__(self, mining_fee=0.5, mining_reward=3, difficulty=4):
        self.users = []
        self.blockchain = []
        self.mempool = []
        self.transactions = []
        self.UTXO_set = []
        self.rewards = []
        self.mining_fees = []
        self.money_in_circulation = {}

        self.mining_fee = mining_fee
        self.mining_reward = mining_reward
        self.difficulty = difficulty

        self.index_user = 0
        self.index_transaction = 0
        self.index_block = 0
        self.index_utxo = 0

        self.first_user = self.create_genesis_block()


    def create_genesis_block(self):
        user0 = self.create_user()
        special_transaction = self.create_coinbase_transaction(
                    miner=user0,  # The first user is the miner of the genesis block
                    amount=1000
                )
        special_transaction.process_transaction()
        genesis_block = Block(
                    index=0,
                    transactions=[special_transaction.serialize_transaction()],
                    previous_hash='0'
                )
        
        self.add_block(genesis_block)
        self.add_transaction(special_transaction)
        self.get_money_circulation(genesis_block)

        return user0

    
    def get_index_utxo(self):
        index = self.index_utxo
        self.index_utxo += 1
        return str(index)
    
    
    def create_user(self):
        user = User(self.index_user)
        self.add_user(user)
        self.index_user += 1
        print(f"User {user.index} created with adress {user.adress}.")
        return user

    
    def add_block(self, block):
        self.blockchain.append(block)
        self.index_block += 1
        print(f"Block {block.index} created and added to blockchain.")


    def add_user(self, user):
        self.users.append(user)


    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        if transaction.sender is None:
            print(f"Coinbase transaction {transaction.index} added: {transaction.receiver.adress} received {transaction.amount}.")
        else:
            print(f"Transaction {transaction.index} added: {transaction.sender.adress} sent {transaction.amount} to {transaction.receiver.adress}.")


    def add_reward(self, reward):
        self.rewards.append(reward)


    def send_transaction(self, sender, receiver, amount):
        transaction = Transaction(
                    index=self.index_transaction,
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    system=self
                )
        if transaction.process_transaction():
            self.add_transaction(transaction)
            self.index_transaction += 1
            self.mempool.append(transaction.serialize_transaction())
            print(f"Transaction {transaction.index} processed: {sender.adress} sent {amount} to {receiver.adress}.")
            return True
        else:
            print("Transaction failed due to insufficient balance or invalid amount.")
            return False


    def get_balances(self):
        balances = {}
        for user in self.users:
            balances[f"Usuario {user.index}"] = [user.adress, user.get_balance(self.UTXO_set)]
        return balances
    

    def get_money_circulation(self, block):
        money_circulation = sum(utxo.amount for utxo in self.UTXO_set)
        self.money_in_circulation[block.timestamp] = money_circulation

    
    def create_coinbase_transaction(self, miner, amount):
        coinbase_transaction = Transaction(
            index=self.index_transaction,
            sender=None,  # Coinbase transaction does not have a sender
            receiver=miner,
            amount=amount,
            system=self
        )
        return coinbase_transaction
    

    def get_mining_fees(self):
        total_fees = sum(tx['mining_fee'] for tx in self.mempool if tx['sender'] is not None)
        return total_fees
    

    def mine_block(self, miner):
        total_reward = self.mining_reward + self.get_mining_fees()

        coinbase_transaction = self.create_coinbase_transaction(miner, total_reward)
        self.transactions.append(coinbase_transaction)
        self.mempool.insert(0, coinbase_transaction.serialize_transaction())

        prev_bloque = self.blockchain[-1]
        prev_hash = prev_bloque.hash
        index = self.index_block

        block = Block(
            index=index,
            transactions=self.mempool,
            previous_hash=prev_hash
        )

        block.miner_total_reward = total_reward

        start_time = time.time()
        while block.hash[:self.difficulty] != '0' * self.difficulty:
            block.nonce = random.randint(0, 1_000_000_000)
            block.hash = block.compute_hash()
        end_time = time.time()
        block.mining_time = round(end_time - start_time, 4)

        print(f"Block mined: {block.hash} by {miner.adress} in {block.mining_time}s")

        coinbase_transaction.process_transaction()
        self.add_block(block)
        self.add_reward(coinbase_transaction)
        self.mempool = []
        self.get_money_circulation(block)

        return block





