import streamlit as st

from database.db import (
    listar_todos_requisitos,
    listar_requisitos_cliente
)


def tabela_requisitos():
    st.title("Requisitos")
    st.divider()
    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    if funcao == "cliente":
        requisitos = listar_requisitos_cliente(id_usuario)
    else:
        requisitos = listar_todos_requisitos()

    for requisito in requisitos:

        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 1])
        with col1:
            st.markdown("**Nome**")
        with col2:
            st.markdown("**Tipo**")
        with col3:
            st.markdown("**Status**")
        with col4:
            if funcao != "cliente":
                st.markdown("**Cliente**")
        with col5:
            if funcao != "cliente":
                st.markdown("**Visível**")

        st.divider()

        with col1:
            st.write(requisito[1])

        with col2:
            st.write(requisito[3])

        with col3:
            st.write(requisito[4])

        with col4:
            if funcao != "cliente":
                st.write(requisito[6])

        with col5:
            if funcao != "cliente":
                st.write("Sim" if requisito[5] else "Não")

        with col6:
            if st.button("Abrir", key=f"req_{requisito[0]}"):
                st.session_state["requisito_selecionado"] = requisito[0]
                st.session_state["pagina_atual"] = "Perfil Requisito"
                st.rerun()