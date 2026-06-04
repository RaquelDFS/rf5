import streamlit as st

from database.db import (
    listar_projetos_por_usuario,
    criar_requisito,
)

from components.tabela_requisitos import tabela_requisitos


def pagina_requisitos():
    funcao     = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    if funcao == "analista":
        st.subheader("Cadastrar Requisito")

        projetos = listar_projetos_por_usuario(id_usuario)

        if not projetos:
            st.warning(
                "Nenhum projeto encontrado. "
                "Cadastre um projeto antes de criar requisitos."
            )
        else:
            projeto_selecionado = st.selectbox(
                "Projeto",
                options=projetos,
                format_func=lambda x: x[1] 
            )

            nome      = st.text_input("Nome")
            descricao = st.text_area("Descrição")

            tipo = st.selectbox(
                "Tipo",
                ["funcional", "nao_funcional"]
            )

            visivel_cliente = st.checkbox(
                "Enviar para aprovação do cliente?",
                value=True
            )

            if st.button("Salvar Requisito"):
                if not nome or not descricao:
                    st.error("Preencha o nome e a descrição antes de salvar.")
                else:
                    criar_requisito(
                        projeto_id=projeto_selecionado[0],
                        nome=nome,
                        descricao=descricao,
                        tipo=tipo,
                        visivel_cliente=1 if visivel_cliente else 0
                    )
                    st.success("Requisito cadastrado.")
                    st.rerun()

        st.divider()

    tabela_requisitos()