import base64
from pathlib import Path

import streamlit as st

from controllers.usuario_controller import UsuarioController


def carregar_logo_base64():
    caminho_logo = Path("assets/logo_reqflow_completo.png")

    if not caminho_logo.exists():
        return None

    with open(caminho_logo, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode("utf-8")


def tela_login():
    usuario_controller = UsuarioController()

    logo_base64 = carregar_logo_base64()

    st.markdown(
        "<div style='height: 40px;'></div>",
        unsafe_allow_html=True
    )

    col_espaco_1, col_centro, col_espaco_2 = st.columns([0.16, 0.68, 0.16])

    with col_centro:
        col_esquerda, col_direita = st.columns([0.46, 0.54], gap="small")


        with col_esquerda:
            if logo_base64:
                html_logo = (
                    "<div class='reqflow-login-left-panel'>"
                        "<div class='reqflow-login-left-content'>"
                            f"<img class='reqflow-login-logo-img' src='data:image/png;base64,{logo_base64}' alt='Logo ReqFlow'>"
                        "</div>"
                    "</div>"
                )
            else:
                html_logo = (
                    "<div class='reqflow-login-left-panel'>"
                        "<div class='reqflow-login-left-content'>"
                            "<div>"
                                "<div class='reqflow-logo-text'>Req<span>Flow</span></div>"
                                "<div class='reqflow-logo-subtitle'>"
                                    "Gestão de requisitos<br>"
                                    "de forma simples e eficiente."
                                "</div>"
                                "<p style='margin-top:18px; color:#DC2626;'>"
                                    "Logo não encontrado em assets/logo_reqflow_completo.png"
                                "</p>"
                            "</div>"
                        "</div>"
                    "</div>"
                )

            st.markdown(
                html_logo,
                unsafe_allow_html=True
            )

        with col_direita:
            with st.form("form_login"):
                st.markdown(
                    (
                        "<div class='reqflow-login-form-title'>"
                            "<h2>Bem-vindo ao <span>ReqFlow</span></h2>"
                            "<p>Faça login para acessar sua conta</p>"
                        "</div>"
                    ),
                    unsafe_allow_html=True
                )

                login = st.text_input(
                    "Usuário",
                    placeholder="Digite seu usuário"
                )

                senha = st.text_input(
                    "Senha",
                    type="password",
                    placeholder="Digite sua senha"
                )

                lembrar = st.checkbox("Lembrar de mim")

                entrar = st.form_submit_button("Entrar")

                if entrar:
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
                        st.error("Usuário ou senha inválidos.")
