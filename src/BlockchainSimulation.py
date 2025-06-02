import streamlit as st
import pandas as pd
import json
from graphviz import Digraph
import plotly.express as px
import plotly.graph_objects as go
import os
import pickle
from pyvis.network import Network
from streamlit.components.v1 import html
import io

from System import System



def save_system(filepath="session.pkl"):
    with open(filepath, 'wb') as f:
        pickle.dump(st.session_state.system, f)
    st.success("✅ System saved successfully.")

def load_system(filepath="session.pkl"):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            system = pickle.load(f)
        st.session_state.system = system
        st.session_state['loaded'] = True
        st.success("✅ System loaded successfully.")
        st.rerun()
    else:
        st.warning("⚠️ File not found.")


def draw_snaking_blockchain(blocks, row_length=4):
    import graphviz
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="LR", splines="line", nodesep="0.6", ranksep="0.8")

    for i, block in enumerate(blocks):
        # Choose fill color
        if block.index == 0:
            color = "#FF4B4B"  # Primary red
        else:
            color = "#393B41"  # Block gray

        label = f"Block {block.index}\nNonce: {block.nonce}\nTransactions: {len(block.transactions)}"
        dot.node(str(block.index), label=label, shape="box", style="filled", fillcolor=color, fontcolor="#FAFAFA")

    for i in range(1, len(blocks)):
        row = i // row_length
        direction = "left" if row % 2 == 1 else "right"
        if direction == "right":
            dot.edge(str(i - 1), str(i))
        else:
            dot.edge(str(i), str(i - 1))  # Reverse

    return dot


# Sidebar navigation
st.sidebar.title("Simulador de Blockchain")
menu = st.sidebar.selectbox("Ir a", ["Inicio", "Resumen", "Usuarios", "Transacciones", "Minería", "Blockchain", "Balances", 'Guardar Estado'])

if st.session_state.get('loaded'):
    st.sidebar.success("Sistema cargado ✅")
elif st.session_state.get('new'):
    st.sidebar.info("Sistema nuevo 🆕")
else: 
    st.sidebar.warning("Crea o carga un sistema para comenzar")


# # Ensure initialization if not already done
# if 'system' not in st.session_state:
#     st.session_state.system = System()
#     st.session_state['loaded'] = False

# Inicio
if menu == "Inicio":
    st.title('⛓️ Simulador de Blockchain')
    st.subheader("Iniciar nuevo sistema o cargar desde archivo")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🆕 Nuevo sistema")
        if st.button("Crear nuevo sistema"):
            st.session_state.system = System()
            st.session_state['new'] = True
            st.success("✅ Sistema nuevo creado.")

    with col2:
        st.markdown("### 📂 Cargar sistema")
        uploaded_file = st.file_uploader("Sube un archivo `.pkl` con el sistema guardado", type="pkl")

        if uploaded_file is not None:
            try:
                system = pickle.load(uploaded_file)
                st.session_state.system = system
                st.session_state['loaded'] = True
                st.success("✅ Sistema cargado desde archivo.")
                # st.experimental_rerun()  # Optional: reload app to refresh state
            except Exception as e:
                st.error(f"❌ Error al cargar el archivo: {e}")

# Resumen
if menu == "Resumen":
    try:
        st.title("📊 Resumen del Sistema")
        x = st.session_state.system
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

    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")



# Usuarios
elif menu == "Usuarios":
    try:
        st.title("💳 Crear nueva Wallet")
        x = st.session_state.system.users

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
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")



# Transacciones
elif menu == "Transacciones":
    try:
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
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")


# Minería
elif menu == "Minería":
    try:
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
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")

# Blockchain
elif menu == "Blockchain":
    try:
        st.title("🔗 Blockchain Viewer")
        blockchain = st.session_state.system.blockchain  # your blockchain object


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



        dot = draw_snaking_blockchain(st.session_state.system.blockchain, row_length=4)
        st.graphviz_chart(dot.source)
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")



# Balances
elif menu == "Balances":
    try:
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
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")


elif menu == 'Guardar Estado':
    try:
        st.header("💾 Guardar el sistema actual")
        x = st.session_state.system

        buffer = io.BytesIO()
        pickle.dump(x, buffer)
        buffer.seek(0)

        download_clicked = st.download_button(
            label="⬇️ Descargar sistema como .pkl",
            data=buffer,
            file_name="sistema.pkl",
            mime="application/octet-stream"
        )

        if download_clicked:
            st.success("✅ Archivo descargado con éxito como sistema.pkl")
    except AttributeError:
        st.error("⚠️ No se ha cargado un sistema. Por favor, crea un nuevo sistema o carga uno existente.")
    except pickle.PicklingError as e:
        st.error("Pickling fallid. Refresca el sistema.")
