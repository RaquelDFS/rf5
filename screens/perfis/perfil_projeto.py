import streamlit as st
import datetime

from database.db import (
    buscar_projeto_por_id,
    atualizar_projeto,
    listar_requisitos_por_projeto
)
from screens.requisitos import pagina_requisitos

def pagina_perfil_projeto():

    if "projeto_selecionado" not in st.session_state:
        st.warning("Nenhum projeto selecionado.")
        return

    projeto = buscar_projeto_por_id(
        st.session_state["projeto_selecionado"]
    )

    if not projeto:
        st.error("Projeto não encontrado.")
        return

    funcao = st.session_state.get("funcao")

    st.title("Perfil do Projeto")
    st.divider()

    if funcao == "cliente":
        st.text_input("Nome",        value=projeto[1],  disabled=True)
        st.text_area("Descrição",    value=projeto[2],  disabled=True)
        st.text_input("Status",      value=projeto[3],  disabled=True)
        st.text_input("Início",      value=projeto[4],  disabled=True)
        st.text_input("Prazo",       value=projeto[5],  disabled=True)

        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "Projetos"
            st.rerun()

    elif funcao == "analista":
        nome      = st.text_input("Nome",      value=projeto[1])
        descricao = st.text_area("Descrição",  value=projeto[2])

        status = st.selectbox(
            "Status",
            [
                "iniciado",
                "em_aprovacao",
                "aprovado",
                "em_construcao",
                "em_atraso",
                "em_revisao",
                "concluido",
                "suspenso",
                "cancelado"
            ],
            index=[
                "iniciado",
                "em_aprovacao",
                "aprovado",
                "em_construcao",
                "em_atraso",
                "em_revisao",
                "concluido",
                "suspenso",
                "cancelado"
            ].index(projeto[3])
        )

        data_inicio = st.date_input(
            "Início",
            value=datetime.date.fromisoformat(projeto[4])
        )
        data_fim_prevista = st.date_input(
            "Prazo",
            value=datetime.date.fromisoformat(projeto[5])
        )

        st.text_input("Responsável", value=projeto[9],  disabled=True)
        st.text_input("Cliente",     value=projeto[10], disabled=True)

        if projeto[6]:
            st.text_input(
                "Formalizado em",
                value=projeto[6],
                disabled=True
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Salvar"):
                atualizar_projeto(
                    projeto[0],
                    nome,
                    descricao,
                    status,
                    str(data_inicio),
                    str(data_fim_prevista)
                )
                st.success("Projeto atualizado.")
                st.rerun()

        with col2:
            if st.button("Voltar"):
                st.session_state["pagina_atual"] = "Projetos"
                st.rerun()

        st.divider()
        pagina_requisitos()
        st.subheader("Requisitos do Projeto")

        requisitos = listar_requisitos_por_projeto(projeto[0])

        if not requisitos:
            st.info("Nenhum requisito cadastrado neste projeto.")
        else:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown("**Nome**")
            with col2:
                st.markdown("**Tipo**")
            with col3:
                st.markdown("**Status**")

            st.divider()

            for req in requisitos:
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.write(req[1])
                with col2:
                    st.write(req[3])
                with col3:
                    st.write(req[4])