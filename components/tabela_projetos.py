import streamlit as st

from database.db import listar_projetos_por_usuario


def tabela_projetos():
    id_usuario = st.session_state.get("id_usuario")

    projetos = listar_projetos_por_usuario(id_usuario)

    if not projetos:
        st.info("Nenhum projeto encontrado.")
        return

    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

    with col1:
        st.markdown("**Nome**")
    with col2:
        st.markdown("**Status**")
    with col3:
        st.markdown("**Início**")
    with col4:
        st.markdown("**Prazo**")

    st.divider()

    for projeto in projetos:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

        with col1:
            st.write(projeto[1])  
        with col2:
            st.write(projeto[3])  
        with col3:
            st.write(projeto[4])  
        with col4:
            st.write(projeto[5])  
        with col5:
            if st.button("Abrir", key=f"proj_{projeto[0]}"):
                st.session_state["projeto_selecionado"] = projeto[0]
                st.session_state["pagina_atual"] = "Perfil Projeto"
                st.rerun()