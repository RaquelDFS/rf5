import streamlit as st

from database.db import (
    buscar_requisito_por_id,
    atualizar_requisito,
    excluir_requisito
)


def pagina_perfil_requisito():

    if "requisito_selecionado" not in st.session_state:
        st.warning("Nenhum requisito selecionado.")
        return

    requisito = buscar_requisito_por_id(
        st.session_state["requisito_selecionado"]
    )

    if not requisito:
        st.error("Requisito não encontrado.")
        return

    # Índices retornados por buscar_requisito_por_id:
    # 0  id
    # 1  nome
    # 2  descricao
    # 3  tipo
    # 4  status
    # 5  visivel_cliente
    # 6  projeto_id
    # 7  id_cliente
    # 8  cliente (login)

    funcao = st.session_state.get("funcao")

    st.title("Perfil do Requisito")
    st.divider()

    # -------------------------------------------------------
    # CLIENTE — somente visualização e aprovação/reprovação
    # -------------------------------------------------------
    if funcao == "cliente":

        st.text_input("Nome",      value=requisito[1], disabled=True)
        st.text_area("Descrição",  value=requisito[2], disabled=True)
        st.text_input("Tipo",      value=requisito[3], disabled=True)
        st.write(f"**Status atual:** {requisito[4]}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Aprovar"):
                atualizar_requisito(
                    requisito[0],
                    requisito[1],
                    requisito[2],
                    requisito[3],
                    "aprovado",
                    0
                )
                st.success("Requisito aprovado.")
                st.rerun()

        with col2:
            if st.button("❌ Reprovar"):
                atualizar_requisito(
                    requisito[0],
                    requisito[1],
                    requisito[2],
                    requisito[3],
                    "reprovado",
                    0
                )
                st.success("Requisito reprovado.")
                st.rerun()

        if st.button("Voltar"):
            st.session_state["pagina_atual"] = "Início"
            st.rerun()

    # -------------------------------------------------------
    # ANALISTA — pode editar e excluir
    # -------------------------------------------------------
    else:

        nome      = st.text_input("Nome",      value=requisito[1])
        descricao = st.text_area("Descrição",  value=requisito[2])

        tipo = st.selectbox(
            "Tipo",
            ["funcional", "nao_funcional"],
            index=0 if requisito[3] == "funcional" else 1
        )

        opcoes_status = [
            "em_analise",
            "aguardando_aprovacao",
            "aprovado",
            "reprovado"
        ]

        status = st.selectbox(
            "Status",
            opcoes_status,
            index=opcoes_status.index(requisito[4])
        )

        visivel = st.checkbox(
            "Visível para o cliente",
            value=bool(requisito[5])
        )

        st.text_input("Cliente", value=requisito[8], disabled=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Salvar"):
                atualizar_requisito(
                    requisito[0],
                    nome,
                    descricao,
                    tipo,
                    status,
                    1 if visivel else 0
                )
                st.success("Requisito atualizado.")
                st.rerun()

        with col2:
            if st.button("Excluir"):
                excluir_requisito(requisito[0])
                st.session_state["pagina_atual"] = "Requisitos"
                st.rerun()

        with col3:
            if st.button("Voltar"):
                st.session_state["pagina_atual"] = "Requisitos"
                st.rerun()