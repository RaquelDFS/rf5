import streamlit as st
import pandas as pd
from database.db import listar_requisitos_cliente
from components.tabela_requisitos import tabela_requisitos
from components.tabela_projetos import tabela_projetos


def inicio_analista():
    tabela_projetos()
    tabela_requisitos()


def inicio_cliente():

    st.subheader("Portal do Cliente")

    requisitos = listar_requisitos_cliente(
        st.session_state["id_usuario"]
    )

    st.subheader("Meus Requisitos")

    if not requisitos:
        st.info("Nenhum requisito encontrado.")
        return

    for requisito in requisitos:

        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

        with col1:
            st.write(requisito[1])

        with col2:
            st.write(requisito[3])

        with col3:
            st.write(requisito[4])

        with col4:
            if st.button("Abrir", key=f"req_{requisito[0]}"):
                st.session_state["requisito_selecionado"] = requisito[0]
                st.session_state["pagina_atual"] = "Perfil Requisito"
                st.rerun()


def pagina_inicio():

    funcao = st.session_state["funcao"]

    st.title("ReqFlow")

    if funcao == "analista":
        inicio_analista()

    elif funcao == "cliente":
        inicio_cliente()