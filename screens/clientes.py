import streamlit as st

from database.db import (
    cadastrar_cliente,
    listar_clientes_gestao,
    atualizar_cliente,
    desativar_cliente
)


def pagina_clientes():
    st.title("Clientes")

    funcao = st.session_state.get("funcao")

    if "form_cliente_id" not in st.session_state:
        st.session_state["form_cliente_id"] = 0

    mensagem_cliente = st.session_state.pop("mensagem_cliente", None)
    if mensagem_cliente:
        st.success(mensagem_cliente)

    # ============================================================
    # CADASTRO DE CLIENTE
    # ============================================================

    if funcao in ["gerente", "analista"]:
        st.subheader("Cadastrar Cliente")

        form_id = st.session_state["form_cliente_id"]

        with st.form(
            f"form_cadastro_cliente_{form_id}",
            clear_on_submit=True
        ):
            nome = st.text_input(
                "Nome do Cliente",
                key=f"nome_cliente_{form_id}"
            )

            email = st.text_input(
                "E-mail",
                key=f"email_cliente_{form_id}"
            )

            login = st.text_input(
                "Login",
                key=f"login_cliente_{form_id}"
            )

            senha = st.text_input(
                "Senha",
                type="password",
                key=f"senha_cliente_{form_id}"
            )

            salvar = st.form_submit_button("Salvar Cliente")

            if salvar:
                sucesso, mensagem = cadastrar_cliente(
                    nome=nome,
                    login=login,
                    senha=senha,
                    email=email
                )

                if sucesso:
                    st.session_state["mensagem_cliente"] = mensagem
                    st.session_state["form_cliente_id"] += 1
                    st.rerun()
                else:
                    st.error(mensagem)

        st.divider()

    else:
        st.info("Seu perfil permite visualizar clientes, mas não cadastrar novos registros.")
        st.divider()

    # ============================================================
    # LISTAGEM DE CLIENTES
    # ============================================================

    st.subheader("Clientes Cadastrados")

    clientes = listar_clientes_gestao()

    if not clientes:
        st.info("Nenhum cliente cadastrado.")
        return

    for cliente in clientes:
        id_cliente = cliente[0]
        nome_cliente = cliente[1]
        login_cliente = cliente[2]
        email_cliente = cliente[3] or ""
        ativo_cliente = cliente[4]

        status_cliente = "Ativo" if ativo_cliente == 1 else "Inativo"

        with st.expander(
            f"{nome_cliente} | Login: {login_cliente} | Status: {status_cliente}"
        ):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**Nome:** {nome_cliente}")
                st.write(f"**Login:** {login_cliente}")
                st.write(f"**E-mail:** {email_cliente if email_cliente else '-'}")
                st.write(f"**Status:** {status_cliente}")

            with col2:
                if st.button(
                    "Visualizar",
                    key=f"visualizar_cliente_{id_cliente}"
                ):
                    st.session_state["cliente_selecionado"] = id_cliente
                    st.session_state["pagina_atual"] = "Perfil Cliente"
                    st.rerun()

            # ====================================================
            # EDIÇÃO DE CLIENTE
            # ====================================================

            if funcao in ["gerente", "analista"]:
                st.markdown("#### Editar Cliente")

                with st.form(f"form_editar_cliente_{id_cliente}"):

                    novo_nome = st.text_input(
                        "Nome",
                        value=nome_cliente,
                        key=f"editar_nome_cliente_{id_cliente}"
                    )

                    novo_email = st.text_input(
                        "E-mail",
                        value=email_cliente,
                        key=f"editar_email_cliente_{id_cliente}"
                    )

                    novo_login = st.text_input(
                        "Login",
                        value=login_cliente,
                        key=f"editar_login_cliente_{id_cliente}"
                    )

                    novo_status = st.selectbox(
                        "Status",
                        options=[1, 0],
                        index=0 if ativo_cliente == 1 else 1,
                        format_func=lambda x: "Ativo" if x == 1 else "Inativo",
                        key=f"editar_status_cliente_{id_cliente}"
                    )

                    salvar_edicao = st.form_submit_button("Salvar Alterações")

                    if salvar_edicao:
                        sucesso, mensagem = atualizar_cliente(
                            id_cliente=id_cliente,
                            nome=novo_nome,
                            login=novo_login,
                            email=novo_email,
                            ativo=novo_status
                        )

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)

                if ativo_cliente == 1:
                    if st.button(
                        "Desativar Cliente",
                        key=f"desativar_cliente_{id_cliente}"
                    ):
                        sucesso, mensagem = desativar_cliente(id_cliente)

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)