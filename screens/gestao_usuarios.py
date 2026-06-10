import streamlit as st

from controllers.usuario_controller import UsuarioController


def tela_gestao_usuarios():
    """Tela administrativa de usuários.

    Esta tela permite que o gerente cadastre, busque, visualize, edite,
    desative, reative e redefina a senha dos usuários do sistema.
    """

    controller = UsuarioController()

    st.title("Gestão de Usuários")

    st.write(
        "Nesta tela, o gerente pode cadastrar, buscar, editar, "
        "desativar, reativar e redefinir senhas dos usuários do sistema."
    )

    if "form_usuario_id" not in st.session_state:
        st.session_state["form_usuario_id"] = 0

    mensagem_usuario = st.session_state.pop("mensagem_usuario", None)
    if mensagem_usuario:
        st.success(mensagem_usuario)

    abas = st.tabs(["Cadastrar Usuário", "Buscar Usuários"])

    # ============================================================
    # ABA 1 - CADASTRAR USUÁRIO
    # ============================================================
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

    # ============================================================
    # ABA 2 - BUSCAR USUÁRIOS
    # ============================================================
    with abas[1]:
        st.subheader("Buscar usuários cadastrados")

        st.info(
            "Digite uma informação para buscar o usuário. "
            "Nenhum usuário será exibido sem uma busca."
        )

        col_busca, col_status = st.columns([2, 1])

        with col_busca:
            termo_busca = st.text_input(
                "Buscar por nome, login, e-mail ou função",
                placeholder="Exemplo: gerente, raquel, cliente, dev..."
            )

        with col_status:
            filtro_status = st.selectbox(
                "Status",
                ["Todos", "Ativos", "Inativos"]
            )

        termo_busca = termo_busca.strip().lower()

        if not termo_busca:
            st.warning("Informe um termo de busca para exibir usuários.")
            return

        if len(termo_busca) < 2:
            st.warning("Digite pelo menos 2 caracteres para realizar a busca.")
            return

        usuarios = controller.listar()

        if not usuarios:
            st.info("Nenhum usuário cadastrado.")
            return

        usuarios_filtrados = []

        for usuario in usuarios:
            id_usuario = usuario[0]
            nome = usuario[1] or ""
            login = usuario[2] or ""
            funcao = usuario[3] or ""
            email = usuario[4] or ""
            ativo = usuario[5]

            status_texto = "ativo" if ativo == 1 else "inativo"

            texto_usuario = (
                f"{nome} {login} {funcao} {email} {status_texto}"
            ).lower()

            encontrou_termo = termo_busca in texto_usuario

            if filtro_status == "Ativos":
                passou_status = ativo == 1
            elif filtro_status == "Inativos":
                passou_status = ativo == 0
            else:
                passou_status = True

            if encontrou_termo and passou_status:
                usuarios_filtrados.append(usuario)

        if not usuarios_filtrados:
            st.info("Nenhum usuário encontrado para a busca realizada.")
            return

        st.success(
            f"{len(usuarios_filtrados)} usuário(s) encontrado(s)."
        )

        for usuario in usuarios_filtrados:
            id_usuario = usuario[0]
            nome = usuario[1]
            login = usuario[2]
            funcao = usuario[3]
            email = usuario[4]
            ativo = usuario[5]

            status = "Ativo" if ativo == 1 else "Inativo"

            with st.expander(f"{nome} | {login} | {funcao} | {status}"):

                # ====================================================
                # FORMULÁRIO DE EDIÇÃO DO USUÁRIO
                # ====================================================
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

                    salvar = st.form_submit_button("Salvar alterações")

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

                st.divider()

                # ====================================================
                # REDEFINIR SENHA PELO GERENTE
                # ====================================================
                st.subheader("Redefinir senha")

                with st.form(f"form_redefinir_senha_{id_usuario}"):

                    nova_senha = st.text_input(
                        "Nova senha",
                        type="password",
                        key=f"nova_senha_{id_usuario}"
                    )

                    confirmar_senha = st.text_input(
                        "Confirmar nova senha",
                        type="password",
                        key=f"confirmar_senha_{id_usuario}"
                    )

                    redefinir_senha = st.form_submit_button("Redefinir senha")

                    if redefinir_senha:

                        if not nova_senha:
                            st.warning("Informe a nova senha.")
                        elif nova_senha != confirmar_senha:
                            st.warning("As senhas não coincidem.")
                        else:
                            sucesso, mensagem = controller.alterar_senha(
                                id_usuario,
                                nova_senha
                            )

                            if sucesso:
                                st.success("Senha redefinida com sucesso.")
                                st.rerun()
                            else:
                                st.warning(mensagem)

                st.divider()

                # ====================================================
                # DESATIVAR OU REATIVAR USUÁRIO
                # ====================================================
                if ativo == 1:
                    if st.button(
                        "Desativar usuário",
                        key=f"btn_desativar_{id_usuario}"
                    ):
                        sucesso, mensagem = controller.desativar(id_usuario)

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.warning(mensagem)
                else:
                    if st.button(
                        "Reativar usuário",
                        key=f"btn_reativar_{id_usuario}"
                    ):
                        sucesso, mensagem = controller.atualizar(
                            id_usuario=id_usuario,
                            nome=nome,
                            login=login,
                            funcao=funcao,
                            email=email,
                            ativo=1
                        )

                        if sucesso:
                            st.success("Usuário reativado com sucesso.")
                            st.rerun()
                        else:
                            st.warning(mensagem)