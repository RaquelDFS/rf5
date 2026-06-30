import streamlit as st
from html import escape

from controllers.usuario_controller import UsuarioController


usuario_controller = UsuarioController()


def texto_seguro(valor):
    if valor is None:
        return "-"

    texto = str(valor).strip()

    if texto == "":
        return "-"

    return texto


def texto_html(valor):
    return escape(texto_seguro(valor))


def exibir_topo_clientes():
    st.markdown(
        """
        <div class="reqflow-page-hero">
            <div class="reqflow-page-hero-pill">
                Gestão de clientes
            </div>
            <div class="reqflow-page-hero-title">
                Clientes
            </div>
            <div class="reqflow-page-hero-text">
                Cadastre, consulte e acompanhe os clientes vinculados aos projetos
                e fluxos de validação da plataforma ReqFlow.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def inicializar_estado_clientes():
    if "form_cliente_id" not in st.session_state:
        st.session_state["form_cliente_id"] = 0

    if "consulta_clientes_realizada" not in st.session_state:
        st.session_state["consulta_clientes_realizada"] = False


def marcar_consulta_clientes():
    st.session_state["consulta_clientes_realizada"] = True


def limpar_consulta_clientes():
    st.session_state["consulta_clientes_realizada"] = False
    st.session_state["filtro_clientes_texto"] = ""
    st.session_state["filtro_clientes_status"] = "Todos"


def formatar_status_cliente(ativo):
    if ativo == 1:
        return "Ativo"

    return "Inativo"


def normalizar_clientes(clientes):
    clientes_normalizados = []

    for cliente in clientes:
        clientes_normalizados.append({
            "id": cliente[0],
            "nome": cliente[1],
            "login": cliente[2],
            "email": cliente[3] if cliente[3] else "",
            "ativo": cliente[4],
            "status": formatar_status_cliente(cliente[4])
        })

    return clientes_normalizados


def aplicar_filtros_clientes(clientes, texto_busca, status_filtro):
    resultado = clientes

    if texto_busca:
        texto_busca = texto_busca.lower()

        resultado = [
            cliente for cliente in resultado
            if texto_busca in str(cliente["nome"]).lower()
            or texto_busca in str(cliente["login"]).lower()
            or texto_busca in str(cliente["email"]).lower()
            or texto_busca in str(cliente["status"]).lower()
        ]

    if status_filtro != "Todos":
        resultado = [
            cliente for cliente in resultado
            if cliente["status"] == status_filtro
        ]

    return resultado


def exibir_info_cliente(label, valor):
    st.markdown(
        f"""
        <div class="reqflow-project-info-box">
            <div class="reqflow-project-info-label">{texto_html(label)}</div>
            <div class="reqflow-project-info-value">{texto_html(valor)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def classe_status_cliente(ativo):
    if ativo == 1:
        return "reqflow-status-green"

    return "reqflow-status-gray"


def exibir_badge_status_cliente(ativo):
    status = formatar_status_cliente(ativo)
    classe_status = classe_status_cliente(ativo)

    st.markdown(
        f"""
        <div class="reqflow-status-wrapper">
            <span class="reqflow-project-status {classe_status}">
                {texto_html(status)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def formulario_cadastro_cliente():
    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Novo cliente</h3>
            <p>Preencha as informações abaixo para cadastrar um cliente no ReqFlow.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    form_id = st.session_state["form_cliente_id"]

    with st.container(border=True):
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

            salvar = st.form_submit_button(
                "Salvar Cliente",
                use_container_width=True
            )

            if salvar:
                sucesso, mensagem = usuario_controller.cadastrar_cliente(
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


def exibir_area_filtros_clientes(clientes):
    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Consulta de clientes</h3>
            <p>Utilize os filtros para localizar clientes por nome, login, e-mail ou status.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        texto_busca = st.text_input(
            "Buscar cliente",
            placeholder="Digite nome, login, e-mail ou status",
            key="filtro_clientes_texto"
        )

    with col2:
        status_filtro = st.selectbox(
            "Filtrar por status",
            ["Todos", "Ativo", "Inativo"],
            key="filtro_clientes_status"
        )

    col_botao1, col_botao2, col_espaco = st.columns([1.4, 1.4, 4])

    with col_botao1:
        st.button(
            "Consultar clientes",
            type="primary",
            use_container_width=True,
            on_click=marcar_consulta_clientes
        )

    with col_botao2:
        st.button(
            "Limpar consulta",
            use_container_width=True,
            on_click=limpar_consulta_clientes
        )

    return texto_busca, status_filtro


def exibir_card_cliente(cliente, funcao):
    with st.container(border=True):
        col_titulo, col_status = st.columns([5, 1.4])

        with col_titulo:
            st.markdown(
                f"""
                <div class="reqflow-project-title">
                    {texto_html(cliente["nome"])}
                </div>
                <div class="reqflow-project-description">
                    Login: {texto_html(cliente["login"])}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_status:
            exibir_badge_status_cliente(cliente["ativo"])

        st.markdown(
            '<div class="reqflow-project-section-space"></div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            exibir_info_cliente("E-mail", cliente["email"] if cliente["email"] else "-")

        with col2:
            exibir_info_cliente("Login", cliente["login"])

        with col3:
            exibir_info_cliente("Status", cliente["status"])

        st.markdown(
            '<div class="reqflow-project-actions-line"></div>',
            unsafe_allow_html=True
        )

        col_espaco, col_botao = st.columns([4.5, 1.6])

        with col_botao:
            if st.button(
                "Visualizar",
                key=f"visualizar_cliente_{cliente['id']}",
                use_container_width=True
            ):
                st.session_state["cliente_selecionado"] = cliente["id"]
                st.session_state["pagina_atual"] = "Perfil Cliente"
                st.rerun()

        if funcao in ["gerente", "analista"]:
            with st.expander("Editar cliente"):
                with st.form(f"form_editar_cliente_{cliente['id']}"):
                    novo_nome = st.text_input(
                        "Nome",
                        value=cliente["nome"],
                        key=f"editar_nome_cliente_{cliente['id']}"
                    )

                    novo_email = st.text_input(
                        "E-mail",
                        value=cliente["email"],
                        key=f"editar_email_cliente_{cliente['id']}"
                    )

                    novo_login = st.text_input(
                        "Login",
                        value=cliente["login"],
                        key=f"editar_login_cliente_{cliente['id']}"
                    )

                    novo_status = st.selectbox(
                        "Status",
                        options=[1, 0],
                        index=0 if cliente["ativo"] == 1 else 1,
                        format_func=lambda x: "Ativo" if x == 1 else "Inativo",
                        key=f"editar_status_cliente_{cliente['id']}"
                    )

                    salvar_edicao = st.form_submit_button(
                        "Salvar alterações",
                        use_container_width=True
                    )

                    if salvar_edicao:
                        sucesso, mensagem = usuario_controller.atualizar_cliente(
                            id_cliente=cliente["id"],
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

                if cliente["ativo"] == 1:
                    if st.button(
                        "Desativar cliente",
                        key=f"desativar_cliente_{cliente['id']}",
                        use_container_width=True
                    ):
                        sucesso, mensagem = usuario_controller.desativar_cliente(
                            cliente["id"]
                        )

                        if sucesso:
                            st.success(mensagem)
                            st.rerun()
                        else:
                            st.error(mensagem)


def exibir_lista_clientes(clientes, funcao):
    if not clientes:
        st.info("Nenhum cliente encontrado com os filtros selecionados.")
        return

    for cliente in clientes:
        exibir_card_cliente(cliente, funcao)


def exibir_resumo_clientes(clientes):
    total = len(clientes)

    ativos = len([
        cliente for cliente in clientes
        if cliente["ativo"] == 1
    ])

    inativos = len([
        cliente for cliente in clientes
        if cliente["ativo"] == 0
    ])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Clientes cadastrados", total)

    with col2:
        st.metric("Ativos", ativos)

    with col3:
        st.metric("Inativos", inativos)


def pagina_clientes():
    inicializar_estado_clientes()

    funcao = st.session_state.get("funcao")

    exibir_topo_clientes()

    mensagem_cliente = st.session_state.pop("mensagem_cliente", None)

    if mensagem_cliente:
        st.success(mensagem_cliente)

    clientes = usuario_controller.listar_clientes_gestao()
    clientes = normalizar_clientes(clientes)

    exibir_resumo_clientes(clientes)

    st.divider()

    if funcao in ["gerente", "analista"]:
        formulario_cadastro_cliente()
        st.divider()
    else:
        st.info("Seu perfil permite visualizar clientes, mas não cadastrar novos registros.")
        st.divider()

    texto_busca, status_filtro = exibir_area_filtros_clientes(clientes)

    if not st.session_state.get("consulta_clientes_realizada", False):
        st.info("Utilize os filtros acima e clique em **Consultar clientes** para visualizar os resultados.")
        return

    clientes_filtrados = aplicar_filtros_clientes(
        clientes,
        texto_busca,
        status_filtro
    )

    st.caption(f"Total encontrado: {len(clientes_filtrados)} cliente(s).")

    exibir_lista_clientes(clientes_filtrados, funcao)