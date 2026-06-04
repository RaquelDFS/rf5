import streamlit as st

from database.db import listar_clientes


def pagina_clientes():

    st.title("Clientes")

    clientes = listar_clientes()

    if not clientes:
        st.info("Nenhum cliente cadastrado.")
        return

    col1, col2 = st.columns([4, 1])

    with col1:
        st.write("**Cliente**")

    with col2:
        st.write("**Ações**")

    st.divider()

    for cliente in clientes:

        id_cliente = cliente[0]
        nome_cliente = cliente[1]

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(nome_cliente)

        with col2:

            if st.button(
                "Visualizar",
                key=f"cliente_{id_cliente}"
            ):

                st.session_state["cliente_selecionado"] = id_cliente
                st.session_state["pagina_atual"] = "Perfil Cliente"

                st.rerun()