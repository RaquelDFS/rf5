import streamlit as st

from controllers.usuario_controller import UsuarioController


def pagina_meu_perfil():

    usuario_controller = UsuarioController()

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

        sucesso, mensagem = usuario_controller.alterar_senha(
            st.session_state["id_usuario"],
            nova_senha
        )

        if sucesso:
            st.success(mensagem)
        else:
            st.error(mensagem)
