import streamlit as st

from controllers.usuario_controller import UsuarioController


def tela_gestao_usuarios():
    """Tela administrativa de usuários.

    Esta tela agora usa a camada Controller/Service para aproximar o projeto
    da estrutura POO, mantendo a interface simples em Streamlit.
    """

    controller = UsuarioController()

    st.title("Gestão de Usuários")

    st.write(
        "Nesta tela, o gerente pode cadastrar, visualizar, editar "
        "e desativar usuários do sistema."
    )

    if "form_usuario_id" not in st.session_state:
        st.session_state["form_usuario_id"] = 0

    mensagem_usuario = st.session_state.pop("mensagem_usuario", None)
    if mensagem_usuario:
        st.success(mensagem_usuario)

    abas = st.tabs(["Cadastrar Usuário", "Usuários Cadastrados"])

    with abas[0]:
        st.subheader("Cadastrar novo usuário")

        form_id = st.session_state["form_usuario_id"]

        with st.form(
            f"form_cadastrar_usuario_{form_id}",
            clear_on_submit=True
        ):
            nome = st.text_input(
                "Nome completo",
                key=f"nome_usuario_{form_id}"
            )

            login = st.text_input(
                "Login",
                key=f"login_usuario_{form_id}"
            )

            senha = st.text_input(
                "Senha",
                type="password",
                key=f"senha_usuario_{form_id}"
            )

            funcao = st.selectbox(
                "Função / Perfil",
                options=[
                    None,
                    "gerente",
                    "analista",
                    "desenvolvedor",
                    "testador",
                    "cliente"
                ],
                index=0,
                format_func=lambda x: "Selecione uma função" if x is None else x,
                key=f"funcao_usuario_{form_id}"
            )

            email = st.text_input(
                "E-mail",
                key=f"email_usuario_{form_id}"
            )

            enviar = st.form_submit_button("Cadastrar usuário")

            if enviar:
                sucesso, mensagem = controller.cadastrar(
                    nome=nome,
                    login=login,
                    senha=senha,
                    funcao=funcao if funcao else "",
                    email=email
                )

                if sucesso:
                    st.session_state["mensagem_usuario"] = mensagem
                    st.session_state["form_usuario_id"] += 1
                    st.rerun()
                else:
                    st.warning(mensagem)

    with abas[1]:
        st.subheader("Usuários cadastrados")

        usuarios = controller.listar()

        if not usuarios:
            st.info("Nenhum usuário cadastrado.")
            return

        for usuario in usuarios:
            id_usuario = usuario[0]
            nome = usuario[1]
            login = usuario[2]
            funcao = usuario[3]
            email = usuario[4]
            ativo = usuario[5]

            status = "Ativo" if ativo == 1 else "Inativo"

            with st.expander(f"{nome} | {funcao} | {status}"):
                with st.form(f"form_editar_usuario_{id_usuario}"):
                    novo_nome = st.text_input(
                        "Nome",
                        value=nome,
                        key=f"nome_{id_usuario}"
                    )

                    novo_login = st.text_input(
                        "Login",
                        value=login,
                        key=f"login_{id_usuario}"
                    )

                    perfis = [
                        "gerente",
                        "analista",
                        "desenvolvedor",
                        "testador",
                        "cliente"
                    ]

                    nova_funcao = st.selectbox(
                        "Função / Perfil",
                        perfis,
                        index=perfis.index(funcao) if funcao in perfis else 0,
                        key=f"funcao_{id_usuario}"
                    )

                    novo_email = st.text_input(
                        "E-mail",
                        value=email if email else "",
                        key=f"email_{id_usuario}"
                    )

                    novo_ativo = st.selectbox(
                        "Status",
                        [1, 0],
                        format_func=lambda x: "Ativo" if x == 1 else "Inativo",
                        index=0 if ativo == 1 else 1,
                        key=f"ativo_{id_usuario}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        salvar = st.form_submit_button("Salvar alterações")

                    with col2:
                        desativar = st.form_submit_button("Desativar usuário")

                    if salvar:
                        sucesso, mensagem = controller.atualizar(
                            id_usuario=id_usuario,
                            nome=novo_nome,
                            login=novo_login,
                            funcao=nova_funcao,
                            email=novo_email,
                            ativo=novo_ativo
                        )

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.warning(mensagem)

                    if desativar:
                        sucesso, mensagem = controller.desativar(id_usuario)

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.warning(mensagem)
