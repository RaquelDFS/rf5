import streamlit as st
from config.navigation import MENUS


def tela_dashboard():

    st.sidebar.title("ReqFlow")

    st.sidebar.write(
        f"Usuário: {st.session_state['usuario']}"
    )

    st.sidebar.write(
        f"Função: {st.session_state['funcao']}"
    )

    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = MENUS[
            st.session_state["funcao"]
        ][0]

    st.sidebar.divider()

    for item in MENUS[st.session_state["funcao"]]:

        if st.sidebar.button(
            item,
            use_container_width=True
        ):
            st.session_state["pagina_atual"] = item
            st.rerun()

    st.sidebar.divider()

    if st.sidebar.button(
        "Sair",
        use_container_width=True
    ):
        st.session_state.clear()
        st.rerun()

    return st.session_state["pagina_atual"]
