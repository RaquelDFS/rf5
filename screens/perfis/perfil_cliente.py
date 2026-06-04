import streamlit as st

from database.db import (
    buscar_cliente_por_id,
    listar_requisitos_cliente
)


def pagina_perfil_cliente():

    if "cliente_selecionado" not in st.session_state:

        st.warning(
            "Nenhum cliente selecionado."
        )

        return

    cliente = buscar_cliente_por_id(
        st.session_state["cliente_selecionado"]
    )

    if not cliente:

        st.error("Cliente não encontrado.")
        return

    st.title("Perfil do Cliente")

    st.write(f"**Usuário:** {cliente[1]}")
    st.write(f"**Função:** {cliente[2]}")

    st.divider()

    st.subheader("Requisitos Associados")

    requisitos = listar_requisitos_cliente(
    cliente[0]
    )

    if not requisitos:

        st.info(
            "Este cliente não possui requisitos cadastrados."
        )

    else:

        dados = []

        for requisito in requisitos:

            dados.append({
                "Título": requisito[1],  # nome
                "Status": requisito[4]   # status
            })

        st.dataframe(
            dados,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    if st.button("← Voltar para Clientes"):

        st.session_state["pagina_atual"] = "Clientes"

        st.rerun()