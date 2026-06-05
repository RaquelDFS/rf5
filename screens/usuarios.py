import streamlit as st
from screens.gestao_usuarios import tela_gestao_usuarios


def pagina_usuarios():
    funcao = st.session_state.get("funcao")

    if funcao == "gerente":
        tela_gestao_usuarios()
    else:
        st.warning("Você não possui permissão para acessar a gestão de usuários.")