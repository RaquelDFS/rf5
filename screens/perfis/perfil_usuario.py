import streamlit as st
from database.db import alterar_senha


def pagina_meu_perfil():

    st.title("Meu Perfil")

    st.write(
        f"Usuário: {st.session_state['usuario']}"
    )

    st.write(
        f"Função: {st.session_state['funcao']}"
    )

    st.divider()

    st.subheader("Alterar Senha")

    nova_senha = st.text_input(
        "Nova senha",
        type="password"
    )

    confirmar_senha = st.text_input(
        "Confirmar senha",
        type="password"
    )

    if st.button("Salvar Nova Senha"):

        if not nova_senha:
            st.error("Informe uma senha.")
            return

        if nova_senha != confirmar_senha:
            st.error("As senhas não coincidem.")
            return

        alterar_senha(
            st.session_state["id_usuario"],
            nova_senha
        )

        st.success(
            "Senha alterada com sucesso."
        )