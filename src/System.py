import random
import time

from User import User
from Transaction import Transaction
from UTXO import UTXO
from Block import Block


class System:
    """
    A class to simulate a basic cryptocurrency ecosystem with blockchain, mining, and transactions.

    Attributes:
        users (list): List of all registered users in the system.
        blockchain (list): List of all blocks in the chain.
        mempool (list): Pool of unconfirmed transactions (including coinbase).
        transactions (list): All processed transactions.
        UTXO_set (list): List of all unspent transaction outputs.
        rewards (list): List of mining rewards (coinbase transactions).
        mining_fees (list): List of mining fees per block (not yet used).
        money_in_circulation (dict): Mapping of timestamps to total money in circulation.

        mining_fee (float): Flat fee added to transactions.
        mining_reward (float): Fixed reward for mining a block.
        difficulty (int): Mining difficulty (number of leading zeroes in hash).

        index_user (int): Running index to assign user IDs.
        index_transaction (int): Running index to assign transaction IDs.
        index_block (int): Running index to assign block IDs.
        index_utxo (int): Running index to assign UTXO IDs.

        first_user (User): The initial user who mines the genesis block.

    Methods:
        create_genesis_block(): Creates the genesis block and first user.
        get_index_utxo(): Returns a unique UTXO index as a string.
        create_user(): Instantiates and registers a new user.
        add_block(block): Adds a mined block to the blockchain.
        add_user(user): Adds a user to the system.
        add_transaction(transaction): Records a transaction and displays info.
        add_reward(reward): Records a mining reward.
        send_transaction(sender, receiver, amount): Sends and processes a transaction.
        get_balances(): Returns current balances for all users.
        get_money_circulation(block): Updates money in circulation after each block.
        create_coinbase_transaction(miner, amount): Creates a coinbase (mining reward) transaction.
        get_mining_fees(): Calculates total mining fees from transactions in the mempool.
        mine_block(miner): Performs proof-of-work to mine a new block and update state.
    """

    
    def __init__(self, mining_fee=0.5, mining_reward=3, difficulty=4):
        """
        Initializes the cryptocurrency system with default parameters.

        Args:
            mining_fee (float): Fee charged per transaction.
            mining_reward (float): Reward given to miners per block.
            difficulty (int): Proof-of-work difficulty (number of leading zeroes in hash).
        """
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
        """
        Creates the first user and mines the genesis block with an initial coinbase transaction.

        Returns:
            User: The user who mined the genesis block.
        """
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
        """
        Returns a unique index for the next UTXO.

        Returns:
            str: A unique UTXO index as a string.
        """
        index = self.index_utxo
        self.index_utxo += 1
        return str(index)
    
    
    def create_user(self):
        """
        Creates a new user, adds them to the system, and assigns a unique index.

        Returns:
            User: The created user.
        """
        user = User(self.index_user)
        self.add_user(user)
        self.index_user += 1
        print(f"User {user.index} created with adress {user.adress}.")
        return user

    
    def add_block(self, block):
        """
        Adds a mined block to the blockchain.

        Args:
            block (Block): The block to be added.
        """
        self.blockchain.append(block)
        self.index_block += 1
        print(f"Block {block.index} created and added to blockchain.")


    def add_user(self, user):
        """
        Adds a user to the system's user list.

        Args:
            user (User): The user to be added.
        """
        self.users.append(user)


    def add_transaction(self, transaction):
        """
        Adds a processed transaction to the system.

        Args:
            transaction (Transaction): The transaction to be recorded.
        """
        self.transactions.append(transaction)
        if transaction.sender is None:
            print(f"Coinbase transaction {transaction.index} added: {transaction.receiver.adress} received {transaction.amount}.")
        else:
            print(f"Transaction {transaction.index} added: {transaction.sender.adress} sent {transaction.amount} to {transaction.receiver.adress}.")


    def add_reward(self, reward):
        """
        Adds a mining reward (coinbase transaction) to the rewards list.

        Args:
            reward (Transaction): The coinbase transaction to be recorded.
        """
        self.rewards.append(reward)


    def send_transaction(self, sender, receiver, amount):
        """
        Creates and processes a new transaction between two users.

        Args:
            sender (User): The user sending the funds.
            receiver (User): The user receiving the funds.
            amount (float): The amount to transfer.

        Returns:
            bool: True if the transaction is successful, False otherwise.
        """
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
        """
        Retrieves the current balance for all users.

        Returns:
            dict: Mapping from user index to their address and current balance.
        """
        balances = {}
        for user in self.users:
            balances[f"Usuario {user.index}"] = [user.adress, user.get_balance(self.UTXO_set)]
        return balances
    

    def get_money_circulation(self, block):
        """
        Calculates and stores the total money in circulation after a block is added.

        Args:
            block (Block): The newly mined block.
        """
        money_circulation = sum(utxo.amount for utxo in self.UTXO_set)
        self.money_in_circulation[block.timestamp] = money_circulation

    
    def create_coinbase_transaction(self, miner, amount):
        """
        Creates a coinbase transaction (mining reward) for a miner.

        Args:
            miner (User): The miner receiving the reward.
            amount (float): The reward amount.

        Returns:
            Transaction: The coinbase transaction.
        """
        coinbase_transaction = Transaction(
            index=self.index_transaction,
            sender=None,  # Coinbase transaction does not have a sender
            receiver=miner,
            amount=amount,
            system=self
        )
        return coinbase_transaction
    

    def get_mining_fees(self):
        """
        Calculates the total mining fees from all valid transactions in the mempool.

        Returns:
            float: The sum of all mining fees.
        """
        total_fees = sum(tx['mining_fee'] for tx in self.mempool if tx['sender'] is not None)
        return total_fees
    

    def mine_block(self, miner):
        """
        Mines a new block using proof-of-work, adds it to the blockchain, and processes rewards.

        Args:
            miner (User): The user who mines the block.

        Returns:
            Block: The newly mined block.
        """
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





