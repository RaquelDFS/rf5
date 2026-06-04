import streamlit as st
from database.db import autenticar_usuario


def tela_login():

    st.title("ReqFlow")

    login = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        usuario = autenticar_usuario(
            login,
            senha
        )

        if usuario:

            st.session_state["id_usuario"] = usuario[0]
            st.session_state["usuario"] = usuario[1]
            st.session_state["funcao"] = usuario[2]
            st.session_state["logado"] = True
            st.session_state["pagina_atual"] = "Início"
            st.rerun()

        else:

            st.error(
                "Usuário ou senha inválidos."
            )