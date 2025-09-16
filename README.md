# 🧱 Blockchain Simulation in Python

<img width="1311" alt="Screenshot 2025-06-01 at 9 10 36 p m" src="https://github.com/user-attachments/assets/41f0215d-67fc-4725-bfc1-9d902605ef2d" />

This project simulates a simplified blockchain system using Python and Streamlit. It includes the main components of a blockchain: users with wallets, transactions, UTXO handling, mining with Proof of Work (PoW), block creation, and an interactive interface.

---

## 🚀 Implemented Features

### 💳 Wallets and Keys

* Each user has a private/public key pair (ECDSA over `secp256k1`).
* The address is generated as the SHA-256 hash of the public key.

### 📤 Transactions and UTXO

* UTXO-based model to track balances and transfers.
* Digital signatures to authorize transactions.
* Support for mining fees.

### 🔗 Blocks and Blockchain

* Each block contains valid transactions, the previous hash, timestamp, and nonce.

### ⛏️ Genesis Block and Mining

* The genesis block delivers 1000 coins to the first user.
* Simplified proof of work: the hash must start with a certain number of zeros.
* Block rewards + fees are granted to the miner through a coinbase transaction.

### 💻 Streamlit Interface

* Create a new system or load an existing one
* View system summary
* Create new wallets
* Send transactions
* Mine blocks
* Visualize the blockchain
* View user balances
* Save the system

---

## 📂 Project Structure

```
README.md
└── src
    ├── Block.py                     # Block definition and hashing
    ├── BlockchainSimulation.py      # Streamlit interface logic
    ├── System.py                    # System controller (users, transactions, mining)
    ├── Transaction.py               # Transaction logic, signatures, and validation
    ├── UTXO.py                      # Unspent Transaction Output (UTXO) model
    └── User.py                      # Wallet and key management
```

---

## 📚 Technologies Used

* Python 3.11
* Streamlit
* ECDSA (Elliptic Curve Cryptography)
* SHA-256 hashing
* Pandas (for data visualization)

---

## 🎥 System Demo

[Click here to watch the demo video](https://drive.google.com/file/d/1irmibxGPKnbp8mnaR5ZVYQXonowl0ZU9/view?usp=sharing)

