# 🧱 Simulación de Blockchain en Python



Este proyecto simula un sistema de blockchain simplificado utilizando Python y Streamlit. Incluye los componentes principales de una cadena de bloques: usuarios con wallets, transacciones, manejo de UTXOs, minería con Prueba de Trabajo (PoW), creación de bloques y una interfaz interactiva.


---

## 🚀 Funcionalidades Implementadas

### 💳 Wallets y Llaves
- Cada usuario tiene un par de llaves privada/pública (ECDSA sobre `secp256k1`).
- La dirección se obtiene como el hash SHA-256 de la llave pública.

### 📤 Transacciones y UTXO
- Modelo basado en UTXOs para rastrear saldos y transferencias.
- Firmas digitales para autorizar transacciones.
- Soporte para comisiones de minería.

### 🔗 Bloques y Blockchain
- Cada bloque contiene transacciones válidas, hash anterior, timestamp y nonce.

### ⛏️ Bloque Génesis y Minería
- El bloque génesis entrega 1000 monedas al primer usuario.
- Prueba de trabajo simplificada: el hash debe empezar con cierta cantidad de ceros.
- Recompensas por bloque + comisiones se entregan al minero a través de una transacción coinbase.

### 💻 Interfaz con Streamlit
- Crear nuevo sistema o cargar uno existente
- Ver resumen del sistema
- Crear nuevas wallets
- Enviar transacciones
- Minar bloques
- Visualizar la cadena de bloques
- Ver saldos de los usuarios
- Guardar el sistema

---

## 📂 Estructura del Proyecto

```
README.md
└── src
    ├── Block.py                     # Definición de bloques y hashing
    ├── BlockchainSimulation.py      # Lógica de la interfaz con Streamlit
    ├── System.py                    # Controlador del sistema (usuarios, transacciones, minería)
    ├── Transaction.py               # Lógica de transacciones, firmas y validación
    ├── UTXO.py                      # Modelo de salidas no gastadas (UTXO)
    └── User.py                      # Gestión de wallets y llaves
````

---

## 📚 Tecnologías Utilizadas

* Python 3.11
* Streamlit
* ECDSA (criptografía de curva elíptica)
* SHA-256 hashing
* Pandas (para visualización de datos)

---

## 🎥 Demo del sistema

[Haz clic aquí para ver la demostración en video](https://drive.google.com/file/d/18IEYmmmUV7B4eFUr93vkB4cuVs6n-mNd/view?usp=sharing)

