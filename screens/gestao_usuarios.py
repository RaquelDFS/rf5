import streamlit as st

from controllers.usuario_controller import UsuarioController


usuario_controller = UsuarioController()


def inicializar_estado_usuarios():
    if "form_usuario_id" not in st.session_state:
        st.session_state["form_usuario_id"] = 0

    if "consulta_usuarios_realizada" not in st.session_state:
        st.session_state["consulta_usuarios_realizada"] = False


def marcar_consulta_usuarios():
    st.session_state["consulta_usuarios_realizada"] = True


def limpar_consulta_usuarios():
    st.session_state["consulta_usuarios_realizada"] = False
    st.session_state["filtro_usuarios_texto"] = ""
    st.session_state["filtro_usuarios_status"] = "Todos"


def formatar_status_usuario(ativo):
    if ativo == 1:
        return "Ativo"

    return "Inativo"


def normalizar_usuarios(usuarios):
    usuarios_normalizados = []

    for usuario in usuarios:
        usuarios_normalizados.append({
            "id": usuario[0],
            "nome": usuario[1],
            "login": usuario[2],
            "funcao": usuario[3],
            "email": usuario[4] if usuario[4] else "",
            "empresa": usuario[5] if len(usuario) > 5 and usuario[5] else "",
            "tipo_cliente": usuario[6] if len(usuario) > 6 and usuario[6] else "",
            "documento": usuario[7] if len(usuario) > 7 and usuario[7] else "",
            "ativo": usuario[8] if len(usuario) > 8 else usuario[5],
            "status": formatar_status_usuario(usuario[8] if len(usuario) > 8 else usuario[5])
        })

    return usuarios_normalizados


def aplicar_filtros_usuarios(usuarios, texto_busca, status_filtro):
    resultado = usuarios

    if texto_busca:
        texto_busca = texto_busca.lower()

        resultado = [
            usuario for usuario in resultado
            if texto_busca in str(usuario["nome"]).lower()
            or texto_busca in str(usuario["login"]).lower()
            or texto_busca in str(usuario["funcao"]).lower()
            or texto_busca in str(usuario["email"]).lower()
            or texto_busca in str(usuario["empresa"]).lower()
            or texto_busca in str(usuario["tipo_cliente"]).lower()
            or texto_busca in str(usuario["documento"]).lower()
            or texto_busca in str(usuario["status"]).lower()
        ]

    if status_filtro != "Todos":
        resultado = [
            usuario for usuario in resultado
            if usuario["status"] == status_filtro
        ]

    return resultado


def exibir_resumo_usuarios(usuarios):
    total = len(usuarios)

    ativos = len([
        usuario for usuario in usuarios
        if usuario["ativo"] == 1
    ])

    inativos = len([
        usuario for usuario in usuarios
        if usuario["ativo"] == 0
    ])

    clientes = len([
        usuario for usuario in usuarios
        if usuario["funcao"] == "cliente"
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Usuários cadastrados", total)

    with col2:
        st.metric("Ativos", ativos)

    with col3:
        st.metric("Inativos", inativos)

    with col4:
        st.metric("Clientes", clientes)


def formulario_cadastro_usuario():
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

        enviar = st.form_submit_button(
            "Cadastrar usuário",
            use_container_width=True
        )

        if enviar:
            sucesso, mensagem = usuario_controller.cadastrar(
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


def exibir_area_filtros_usuarios():
    st.subheader("Buscar usuários cadastrados")

    st.info(
        "Utilize os filtros abaixo e clique em Consultar usuários para visualizar os resultados."
    )

    col_busca, col_status = st.columns([2, 1])

    with col_busca:
        texto_busca = st.text_input(
            "Buscar por nome, login, e-mail, função ou empresa",
            placeholder="Exemplo: gerente, raquel, cliente, dev, Clínica...",
            key="filtro_usuarios_texto"
        )

    with col_status:
        filtro_status = st.selectbox(
            "Status",
            ["Todos", "Ativo", "Inativo"],
            key="filtro_usuarios_status"
        )

    col_botao1, col_botao2, col_espaco = st.columns([1.4, 1.4, 4])

    with col_botao1:
        st.button(
            "Consultar usuários",
            type="primary",
            use_container_width=True,
            on_click=marcar_consulta_usuarios
        )

    with col_botao2:
        st.button(
            "Limpar consulta",
            use_container_width=True,
            on_click=limpar_consulta_usuarios
        )

    return texto_busca, filtro_status


def formulario_edicao_usuario(usuario):
    id_usuario = usuario["id"]
    nome = usuario["nome"]
    login = usuario["login"]
    funcao = usuario["funcao"]
    email = usuario["email"]
    ativo = usuario["ativo"]

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

        salvar = st.form_submit_button(
            "Salvar alterações",
            use_container_width=True
        )

        if salvar:
            sucesso, mensagem = usuario_controller.atualizar(
                id_usuario=id_usuario,
                nome=novo_nome,
                login=novo_login,
                funcao=nova_funcao,
                email=novo_email,
                ativo=novo_ativo,
                empresa=usuario["empresa"],
                tipo_cliente=usuario["tipo_cliente"],
                documento=usuario["documento"]
            )

            if sucesso:
                st.success(mensagem)
                st.rerun()
            else:
                st.warning(mensagem)


def formulario_redefinir_senha(usuario):
    id_usuario = usuario["id"]

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

        redefinir_senha = st.form_submit_button(
            "Redefinir senha",
            use_container_width=True
        )

        if redefinir_senha:
            if not nova_senha:
                st.warning("Informe a nova senha.")
            elif nova_senha != confirmar_senha:
                st.warning("As senhas não coincidem.")
            else:
                sucesso, mensagem = usuario_controller.alterar_senha(
                    id_usuario,
                    nova_senha
                )

                if sucesso:
                    st.success("Senha redefinida com sucesso.")
                    st.rerun()
                else:
                    st.warning(mensagem)


def botoes_status_usuario(usuario):
    id_usuario = usuario["id"]
    nome = usuario["nome"]
    login = usuario["login"]
    funcao = usuario["funcao"]
    email = usuario["email"]
    ativo = usuario["ativo"]

    if ativo == 1:
        if st.button(
            "Desativar usuário",
            key=f"btn_desativar_{id_usuario}",
            use_container_width=True
        ):
            sucesso, mensagem = usuario_controller.desativar(id_usuario)

            if sucesso:
                st.success(mensagem)
                st.rerun()
            else:
                st.warning(mensagem)
    else:
        if st.button(
            "Reativar usuário",
            key=f"btn_reativar_{id_usuario}",
            use_container_width=True
        ):
            sucesso, mensagem = usuario_controller.atualizar(
                id_usuario=id_usuario,
                nome=nome,
                login=login,
                funcao=funcao,
                email=email,
                ativo=1,
                empresa=usuario["empresa"],
                tipo_cliente=usuario["tipo_cliente"],
                documento=usuario["documento"]
            )

            if sucesso:
                st.success("Usuário reativado com sucesso.")
                st.rerun()
            else:
                st.warning(mensagem)


def exibir_card_usuario(usuario):
    status = usuario["status"]
    complemento_cliente = ""

    if usuario["funcao"] == "cliente" and usuario["empresa"]:
        complemento_cliente = f" | {usuario['empresa']}"

    with st.expander(
        f"{usuario['nome']} | {usuario['login']} | {usuario['funcao']} | {status}{complemento_cliente}"
    ):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Nome**")
            st.write(usuario["nome"])

        with col2:
            st.write("**Login**")
            st.write(usuario["login"])

        with col3:
            st.write("**Status**")
            st.write(status)

        col4, col5 = st.columns(2)

        with col4:
            st.write("**Função**")
            st.write(usuario["funcao"])

        with col5:
            st.write("**E-mail**")
            st.write(usuario["email"] if usuario["email"] else "-")

        if usuario["funcao"] == "cliente":
            col6, col7, col8 = st.columns(3)

            with col6:
                st.write("**Empresa**")
                st.write(usuario["empresa"] if usuario["empresa"] else "-")

            with col7:
                st.write("**Tipo**")
                st.write(usuario["tipo_cliente"] if usuario["tipo_cliente"] else "-")

            with col8:
                st.write("**Documento**")
                st.write(usuario["documento"] if usuario["documento"] else "-")

        st.divider()

        formulario_edicao_usuario(usuario)

        st.divider()

        formulario_redefinir_senha(usuario)

        st.divider()

        botoes_status_usuario(usuario)


def exibir_lista_usuarios(usuarios):
    if not usuarios:
        st.info("Nenhum usuário encontrado com os filtros selecionados.")
        return

    for usuario in usuarios:
        exibir_card_usuario(usuario)


def tela_gestao_usuarios():
    inicializar_estado_usuarios()

    st.title("Gestão de Usuários")

    st.write(
        "Nesta tela, o gerente pode cadastrar, buscar, editar, "
        "desativar, reativar e redefinir senhas dos usuários do sistema."
    )

    mensagem_usuario = st.session_state.pop("mensagem_usuario", None)

    if mensagem_usuario:
        st.success(mensagem_usuario)

    usuarios = usuario_controller.listar()
    usuarios = normalizar_usuarios(usuarios)

    exibir_resumo_usuarios(usuarios)

    abas = st.tabs(["Cadastrar Usuário", "Buscar Usuários"])

    with abas[0]:
        formulario_cadastro_usuario()

    with abas[1]:
        texto_busca, filtro_status = exibir_area_filtros_usuarios()

        if not st.session_state.get("consulta_usuarios_realizada", False):
            st.info(
                "Utilize os filtros acima e clique em **Consultar usuários** para visualizar os resultados."
            )
            return

        usuarios_filtrados = aplicar_filtros_usuarios(
            usuarios,
            texto_busca.strip(),
            filtro_status
        )

        st.caption(
            f"Total encontrado: {len(usuarios_filtrados)} usuário(s)."
        )

        exibir_lista_usuarios(usuarios_filtrados)
