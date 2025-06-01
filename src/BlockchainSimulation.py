import streamlit as st
import pandas as pd
import json
from graphviz import Digraph
import plotly.express as px
import os
import pickle

from User import User
from Transaction import Transaction
from UTXO import UTXO
from Block import Block
from System import System



def save_session_state():
    try:
        with open('../temp/session_state/session_state.pkl', 'wb') as f:
            pickle.dump({'system': st.session_state.system}, f)
            print("✅ Saved system state.")
            return True
    except Exception as e:
        print("❌ Error saving state:", e)
        return False


def load_session_state():
    try:
        with open('../temp/session_state/session_state.pkl', 'rb') as f:
            loaded_state = pickle.load(f)
            print("✅ Loaded session state.")
            return loaded_state['system']  # Return the actual System object
    except Exception as e:
        print("❌ Error loading session:", e)
    return None



# Initialize system state if not already
if 'system' not in st.session_state:
    st.session_state.system = System()
    st.session_state['loaded'] = False 


# Sidebar navigation
st.sidebar.title("Simulador de Blockchain")
menu = st.sidebar.selectbox("Ir a", ["Inicio", "Usuarios", "Transacciones", "Minería", "Blockchain", "Balances", 'Guardar/Cargar Estado'])

# Inicio
if menu == "Inicio":
    st.title("📊 Resumen del Sistema")
    st.text("")
    st.text("")    
    st.text("")
    st.text("")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Recompensa de Minería", st.session_state.system.mining_reward)
    col2.metric("🧾 Tarifa de Minería", st.session_state.system.mining_fee)
    col3.metric("🛠️ Dificultad de Minería", st.session_state.system.difficulty)

    col4, col5, col6 = st.columns(3)
    col4.metric("👥 Usuarios", len(st.session_state.system.users))
    col5.metric("📦 Bloques en la cadena", len(st.session_state.system.blockchain))
    col6.metric("🔄 Transacciones pendientes", len(st.session_state.system.mempool))

    col7, col8, col9 = st.columns(3)
    col7.metric("✅ Transacciones confirmadas", sum(len(block.transactions) for block in st.session_state.system.blockchain)) #sum(len(block.transactions) for block in system.blockchain)
    col8.metric("🧱 UTXOs disponibles", len(st.session_state.system.UTXO_set))
    col9.metric("🏆 Recompensas totales", sum(utxo.amount for utxo in st.session_state.system.rewards))

    col10, col11, col13 = st.columns(3)
    with col11:
        balances_dict = st.session_state.system.get_balances()
        total = sum(user_info[1] for user_info in balances_dict.values())
        col11.metric(f"### 💰 Total en circulación", round(total, 4))

    
    money_in_circulation = st.session_state.system.money_in_circulation  
    if money_in_circulation:

   
        money_in_circulation_data = []
        for key, value in money_in_circulation.items():
            date = key
            money = value  
            money_in_circulation_data.append({
                'Index': date,  
                'Amount': money
            })

        df_money_in_circulation = pd.DataFrame(money_in_circulation_data)
        df_money_in_circulation['Index'] = pd.to_datetime(df_money_in_circulation['Index'])

        # Plot line chart
        fig = px.line(df_money_in_circulation, x='Index', y='Amount', title="💸 Dinero en Circulación",
                    labels={"Index": "Fecha", "Amount": "Dinero"}, markers=True)

        fig.update_layout(
            xaxis=dict(
                tickformat="%Y-%m-%d\n%H:%M:%S", 
                tickangle=45
            )
        )

        st.plotly_chart(fig)



    rewards = st.session_state.system.rewards  
    if rewards:

        reward_data = []
        for i, utxo in enumerate(rewards):
            reward_data.append({
                'Index': i,  
                'Amount': utxo.amount
            })

        df_rewards = pd.DataFrame(reward_data)

        fig = px.line(df_rewards, x="Index", y="Amount", title="🏆 Recompensas por Bloque",
                    labels={"Index": "Bloque", "Amount": "Recompensa"}, markers=True)
        fig.update_layout(
                    xaxis=dict(
                        range=[-1, df_rewards["Index"].max() + 1],
                        tick0=0,      # starting tick
                        dtick=1       # step size
                    )
                )


        total = sum(utxo.amount for utxo in rewards)
        st.plotly_chart(fig)




# Usuarios
elif menu == "Usuarios":
    st.title("💳 Crear nueva Wallet")

    if st.button("➕ Crear usuario"):
        new_user = st.session_state.system.create_user()
        st.success(f"✅ Usuario {new_user.index} creado correctamente")

        with st.expander("📬 Detalles de la nueva Wallet", expanded=True):
            st.code(f"Usuario {new_user.index}", language="text")
            st.code(f"Dirección: {new_user.adress}", language="text")

    st.subheader("👥 Usuarios Registrados")
    if not st.session_state.system.users:
        st.info("Aún no hay usuarios registrados.")
    else:
        for user in st.session_state.system.users:
            with st.expander(f"👤 Usuario {user.index}"):
                st.text(f"📍 Dirección:\n{user.adress}")
                balance = user.get_balance(st.session_state.system.UTXO_set)
                st.metric("💰 Saldo", balance)


# Transacciones
elif menu == "Transacciones":
    st.title("📤 Enviar Transacción")

    users = st.session_state.system.users
    utxo_set = st.session_state.system.UTXO_set

    if len(users) < 2:
        st.warning("❌ Necesitas al menos 2 usuarios para enviar transacciones.")
    else:
        sender = st.selectbox("👤 Remitente", users, format_func=lambda x: f"Usuario {x.index}")
        balance = float(sender.get_balance(utxo_set))
        max_value = balance - st.session_state.system.mining_fee
        receiver = st.selectbox("👥 Receptor", [u for u in users if u.adress != sender.adress], format_func=lambda x: f"Usuario {x.index}")

        col1, col2 = st.columns([2, 1])
        with col1:
            if max_value <= 0:
                st.warning("⚠️ El remitente no tiene saldo suficiente para enviar transacciones.")
            else:
                amount = st.number_input("💸 Cantidad a enviar", min_value=0.1, max_value=max_value, step=5.0)

        with col2:
            st.metric("💰 Saldo del remitente", round(balance, 2))

        if max_value > 0 and sender.adress != receiver.adress:
            if st.button("📨 Enviar"):
                success = st.session_state.system.send_transaction(sender, receiver, amount)
                if success:
                    st.success("✅ Transacción enviada correctamente.")
                else:
                    st.error("❌ Falló el envío de la transacción.")
        elif sender.adress == receiver.adress:
            st.warning("⚠️ El remitente y el receptor no pueden ser la misma persona.")


# Minería
elif menu == "Minería":
    st.title("⛏️ Minar Bloque")
    if not st.session_state.system.mempool:
        st.warning("No hay transacciones pendientes")
    else:
        col1, col2, col3 = st.columns([1, 0.1, 0.4])
        with col1:
            users = st.session_state.system.users
            minero = st.selectbox("Selecciona minero para recibir la recompensa", users, format_func=lambda x: f"Usuario {x.index}")
            if st.button("⚒️ Minar Bloque"):
                block = st.session_state.system.mine_block(minero)
                st.success("Bloque minado y añadido a la cadena")
                st.write(f"⏱️ Tiempo de minería: {block.mining_time:.2f} segundos")
                st.write(f"💰 Recompensa total del minero: {block.miner_total_reward}")
        with col3:
            col3.metric("🔄 Transacciones pendientes", len(st.session_state.system.mempool))

# Blockchain
elif menu == "Blockchain":
    blockchain = st.session_state.system.blockchain  # your blockchain object

    st.title("🔗 Blockchain Viewer")

    for block in blockchain:
        with st.expander(f"🧱 Block {block.index}"):
            st.markdown(f"**Index:** {block.index}")
            st.markdown(f"**Timestamp:** {block.timestamp}")
            st.markdown(f"**Previous Hash:** `{block.previous_hash}`")
            st.markdown(f"**Hash:** `{block.hash}`")
            st.markdown(f"**Nonce:** {block.nonce}")
            st.markdown(f"**Miner Reward:** {block.miner_total_reward}")
            st.markdown(f"**Mining Time:** {block.mining_time}")
            
            st.markdown("**Transactions:**")
            for tx in block.transactions:
                st.code(json.dumps(tx, indent=2), language="json")

    dot = Digraph(comment='Blockchain')


# Balances
elif menu == "Balances":
    st.title("🏦 Saldos Actuales")

    balances_dict = st.session_state.system.get_balances()

    data = []
    for user, info in balances_dict.items():
        balance = float(info[1])
        address = info[0]
        data.append({"Usuario": user, "Dirección": address, "Saldo": round(balance, 4)})

    df = pd.DataFrame(data)
    df = df.sort_values(by="Saldo", ascending=False)

    st.dataframe(df, use_container_width=True, hide_index=True)

    a, b, c = st.columns(3)
    with b:
        total = sum(user_info[1] for user_info in balances_dict.values())
        st.metric(f"### 💰 Total en circulación", round(total, 4))


elif menu == 'Guardar/Cargar Estado':
    st.title("💾 Guardar y Cargar Estado del Sistema")

    if st.button("Guardar Estado"):
        if save_session_state():
            st.success("✅ Estado guardado correctamente.")
        else:
            st.error("❌ No se pudo guardar el estado.")

    if st.button("Cargar Estado"):
        new_system = load_session_state()
        if new_system:
            st.session_state.system = new_system
            st.success("✅ Estado cargado correctamente. Recargando...")
            st.rerun()  # <- updated for newer Streamlit versions
        else:
            st.error("❌ No se pudo cargar el estado.")

