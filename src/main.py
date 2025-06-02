from User import User
from Transaction import Transaction
from UTXO import UTXO
from Block import Block
from System import System


def main():
    print('System details:')
    print('Mining Fee:', 0.5)
    print('Mining Reward:', 3)
    print('Difficulty:', 4)
    system = System()
    user0 = system.first_user
    user1 = system.create_user()
    miner = system.create_user()
    print('User 0 Balance:', user0.get_balance(system.UTXO_set))

    system.send_transaction(
        sender=user0,
        receiver=user1,
        amount=50
    )

    print('User 0 Balance:', user0.get_balance(system.UTXO_set))
    print('User 1 Balance:', user1.get_balance(system.UTXO_set))

    system.mine_block(miner)

    print('User 0 Balance:', user0.get_balance(system.UTXO_set))
    print('User 1 Balance:', user1.get_balance(system.UTXO_set))
    print('User 3 Balance:', miner.get_balance(system.UTXO_set))
    

if __name__ == "__main__":
    main()