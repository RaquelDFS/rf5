import streamlit as st

from controllers.usuario_controller import UsuarioController


def tela_login():

    usuario_controller = UsuarioController()

    st.title("ReqFlow")

    login = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar"):

        usuario = usuario_controller.autenticar(
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
