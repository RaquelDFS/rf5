import streamlit as st

from database.db import (
    listar_clientes,
    criar_projeto
)

from components.tabela_projetos import tabela_projetos


def pagina_projetos():
    funcao     = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    if funcao == "analista":
        st.subheader("Cadastrar Projeto")

        clientes = listar_clientes()

        if not clientes:
            st.warning("Nenhum cliente cadastrado. Cadastre um cliente antes de criar um projeto.")
        else:
            cliente_selecionado = st.selectbox(
                "Cliente",
                options=clientes,
                format_func=lambda x: x[1]
            )

            nome      = st.text_input("Nome do Projeto")
            descricao = st.text_area("Descrição")

            col1, col2 = st.columns(2)

            with col1:
                data_inicio = st.date_input("Data de Início")
            with col2:
                data_fim_prevista = st.date_input("Data de Término Prevista")

            if st.button("Salvar Projeto"):
                if not nome or not descricao:
                    st.error("Preencha todos os campos antes de salvar.")
                else:
                    criar_projeto(
                        nome,
                        descricao,
                        str(data_inicio),
                        str(data_fim_prevista),
                        id_responsavel=id_usuario,
                        id_cliente=cliente_selecionado[0]
                    )
                    st.success("Projeto cadastrado.")
                    st.rerun()

        st.divider()

    st.subheader("Projetos")
    tabela_projetos()