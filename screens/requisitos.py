import streamlit as st
from html import escape

from controllers.projeto_controller import ProjetoController
from controllers.requisito_controller import RequisitoController
from controllers.historico_controller import HistoricoController


projeto_controller = ProjetoController()
requisito_controller = RequisitoController()
historico_controller = HistoricoController()


def texto_seguro(valor):
    if valor is None:
        return "-"

    texto = str(valor).strip()

    if texto == "":
        return "-"

    return texto


def texto_html(valor):
    return escape(texto_seguro(valor))


def formatar_status(status):
    mapa = {
        "em_analise": "Em análise",
        "aguardando_aprovacao": "Aguardando aprovação",
        "aprovado": "Aprovado",
        "reprovado": "Reprovado"
    }

    return mapa.get(status, status)


def formatar_tipo(tipo):
    mapa = {
        "funcional": "Funcional",
        "nao_funcional": "Não funcional"
    }

    return mapa.get(tipo, tipo)


def formatar_visibilidade(valor):
    if valor == 1 or valor is True:
        return "Sim"

    return "Não"


def classe_status_requisito(status):
    status_texto = str(status).lower()

    if "aprovado" in status_texto:
        return "reqflow-status-green"

    if "aguardando" in status_texto:
        return "reqflow-status-yellow"

    if "reprovado" in status_texto:
        return "reqflow-status-red"

    if "analise" in status_texto or "análise" in status_texto:
        return "reqflow-status-blue"

    return "reqflow-status-gray"


def exibir_badge_status(status):
    status_formatado = formatar_status(status)
    classe_status = classe_status_requisito(status_formatado)

    st.markdown(
        f"""
        <div class="reqflow-status-wrapper">
            <span class="reqflow-project-status {classe_status}">
                {texto_html(status_formatado)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_info_box(label, valor):
    st.markdown(
        f"""
        <div class="reqflow-project-info-box">
            <div class="reqflow-project-info-label">{texto_html(label)}</div>
            <div class="reqflow-project-info-value">{texto_html(valor)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_topo_requisitos():
    st.markdown(
        """
        <div class="reqflow-page-hero">
            <div class="reqflow-page-hero-pill">
                Gestão de requisitos
            </div>
            <div class="reqflow-page-hero-title">
                Requisitos
            </div>
            <div class="reqflow-page-hero-text">
                Cadastre, consulte e acompanhe os requisitos vinculados aos projetos,
                clientes e fluxos de validação da plataforma ReqFlow.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def inicializar_estado_consulta_requisitos():
    if "consulta_requisitos_realizada" not in st.session_state:
        st.session_state["consulta_requisitos_realizada"] = False


def marcar_consulta_requisitos():
    st.session_state["consulta_requisitos_realizada"] = True


def limpar_consulta_requisitos():
    st.session_state["consulta_requisitos_realizada"] = False
    st.session_state["filtro_requisitos_texto"] = ""
    st.session_state["filtro_requisitos_tipo"] = "Todos"
    st.session_state["filtro_requisitos_status"] = "Todos"
    st.session_state["filtro_requisitos_visibilidade"] = "Todos"


def normalizar_requisitos(requisitos, funcao):
    requisitos_normalizados = []

    for requisito in requisitos:
        if funcao == "cliente":
            requisitos_normalizados.append({
                "id": requisito[0],
                "nome": requisito[1],
                "descricao": requisito[2],
                "tipo": requisito[3],
                "status": requisito[4],
                "visivel_cliente": 1,
                "projeto": "",
                "cliente": ""
            })
        else:
            requisitos_normalizados.append({
                "id": requisito[0],
                "nome": requisito[1],
                "descricao": requisito[2],
                "tipo": requisito[3],
                "status": requisito[4],
                "visivel_cliente": requisito[5],
                "projeto": requisito[6],
                "cliente": requisito[7]
            })

    return requisitos_normalizados


def aplicar_filtros_requisitos(
    requisitos,
    texto_busca,
    tipo_filtro,
    status_filtro,
    visibilidade_filtro
):
    resultado = requisitos

    if texto_busca:
        texto_busca = texto_busca.lower()

        resultado = [
            requisito for requisito in resultado
            if texto_busca in str(requisito["nome"]).lower()
            or texto_busca in str(requisito["descricao"]).lower()
            or texto_busca in str(requisito["tipo"]).lower()
            or texto_busca in str(requisito["status"]).lower()
            or texto_busca in str(requisito["projeto"]).lower()
            or texto_busca in str(requisito["cliente"]).lower()
        ]

    if tipo_filtro != "Todos":
        resultado = [
            requisito for requisito in resultado
            if requisito["tipo"] == tipo_filtro
        ]

    if status_filtro != "Todos":
        resultado = [
            requisito for requisito in resultado
            if requisito["status"] == status_filtro
        ]

    if visibilidade_filtro == "Visível para o cliente":
        resultado = [
            requisito for requisito in resultado
            if requisito["visivel_cliente"] == 1
        ]

    elif visibilidade_filtro == "Não visível para o cliente":
        resultado = [
            requisito for requisito in resultado
            if requisito["visivel_cliente"] == 0
        ]

    return resultado


def formulario_cadastro_requisito(id_usuario):
    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Novo requisito</h3>
            <p>Preencha as informações abaixo para cadastrar um requisito vinculado a um projeto.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    projetos = projeto_controller.listar_por_usuario(id_usuario)

    if not projetos:
        st.warning(
            "Nenhum projeto encontrado. "
            "Cadastre um projeto antes de criar requisitos."
        )
        return

    with st.container(border=True):
        with st.form("form_cadastro_requisito", clear_on_submit=True):
            projeto_selecionado = st.selectbox(
                "Projeto",
                options=[None] + projetos,
                index=0,
                format_func=lambda x: "Selecione um projeto" if x is None else x[1]
            )

            nome = st.text_input(
                "Nome",
                placeholder="Ex.: Login do usuário"
            )

            descricao = st.text_area(
                "Descrição",
                placeholder="Descreva o comportamento esperado, regra de negócio ou necessidade do requisito."
            )

            tipo = st.selectbox(
                "Tipo",
                options=[None, "funcional", "nao_funcional"],
                index=0,
                format_func=lambda x: "Selecione o tipo" if x is None else formatar_tipo(x)
            )

            enviar_para_cliente = st.checkbox(
                "Enviar para aprovação do cliente?",
                value=False
            )

            salvar = st.form_submit_button("Salvar requisito", use_container_width=True)

            if salvar:
                if projeto_selecionado is None:
                    st.error("Selecione um projeto antes de salvar.")
                    return

                sucesso, resultado = requisito_controller.criar(
                    projeto_id=projeto_selecionado[0],
                    nome=nome,
                    descricao=descricao,
                    tipo=tipo,
                    enviar_para_cliente=enviar_para_cliente
                )

                if not sucesso:
                    st.error(resultado)
                    return

                status_inicial = (
                    "aguardando_aprovacao"
                    if enviar_para_cliente
                    else "em_analise"
                )

                historico_controller.registrar(
                    tipo_entidade="requisito",
                    id_entidade=resultado,
                    id_usuario=id_usuario,
                    acao="Requisito criado",
                    descricao=(
                        f"Requisito '{nome.strip()}' criado no projeto "
                        f"'{projeto_selecionado[1]}' com status "
                        f"'{formatar_status(status_inicial)}'."
                    )
                )

                st.success("Requisito cadastrado com sucesso.")
                st.rerun()


def exibir_area_filtros(requisitos, funcao):
    inicializar_estado_consulta_requisitos()

    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Consulta de requisitos</h3>
            <p>Utilize os filtros para localizar requisitos por nome, descrição, tipo, status, projeto ou cliente.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        texto_busca = st.text_input(
            "Buscar requisito",
            placeholder="Digite nome, descrição, tipo, status, projeto ou cliente",
            key="filtro_requisitos_texto"
        )

    with col2:
        tipos_disponiveis = sorted(set([requisito["tipo"] for requisito in requisitos]))

        tipo_filtro = st.selectbox(
            "Filtrar por tipo",
            ["Todos"] + tipos_disponiveis,
            format_func=lambda x: x if x == "Todos" else formatar_tipo(x),
            key="filtro_requisitos_tipo"
        )

    col3, col4 = st.columns(2)

    with col3:
        status_disponiveis = sorted(set([requisito["status"] for requisito in requisitos]))

        status_filtro = st.selectbox(
            "Filtrar por status",
            ["Todos"] + status_disponiveis,
            format_func=lambda x: x if x == "Todos" else formatar_status(x),
            key="filtro_requisitos_status"
        )

    with col4:
        if funcao == "cliente":
            visibilidade_filtro = "Todos"
            st.selectbox(
                "Visibilidade",
                ["Todos"],
                disabled=True,
                key="filtro_requisitos_visibilidade_cliente"
            )
        else:
            visibilidade_filtro = st.selectbox(
                "Visibilidade",
                [
                    "Todos",
                    "Visível para o cliente",
                    "Não visível para o cliente"
                ],
                key="filtro_requisitos_visibilidade"
            )

    col_botao1, col_botao2, col_espaco = st.columns([1.4, 1.4, 4])

    with col_botao1:
        st.button(
            "Consultar requisitos",
            type="primary",
            use_container_width=True,
            on_click=marcar_consulta_requisitos
        )

    with col_botao2:
        st.button(
            "Limpar consulta",
            use_container_width=True,
            on_click=limpar_consulta_requisitos
        )

    return texto_busca, tipo_filtro, status_filtro, visibilidade_filtro


def exibir_card_requisito(requisito, funcao):
    nome = texto_seguro(requisito["nome"])
    descricao = texto_seguro(requisito["descricao"])
    tipo = formatar_tipo(requisito["tipo"])
    status = formatar_status(requisito["status"])
    projeto = texto_seguro(requisito["projeto"])
    cliente = texto_seguro(requisito["cliente"])
    visivel_cliente = formatar_visibilidade(requisito["visivel_cliente"])

    with st.container(border=True):
        col_titulo, col_status = st.columns([5, 1.5])

        with col_titulo:
            st.markdown(
                f"""
                <div class="reqflow-requirement-title">
                    {texto_html(nome)}
                </div>
                <div class="reqflow-requirement-description">
                    {texto_html(descricao)}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_status:
            exibir_badge_status(requisito["status"])

        st.markdown('<div class="reqflow-project-section-space"></div>', unsafe_allow_html=True)

        if funcao == "cliente":
            col1, col2 = st.columns(2)

            with col1:
                exibir_info_box("Tipo", tipo)

            with col2:
                exibir_info_box("Status", status)

        else:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                exibir_info_box("Tipo", tipo)

            with col2:
                exibir_info_box("Projeto", projeto)

            with col3:
                exibir_info_box("Cliente", cliente)

            with col4:
                exibir_info_box("Visível", visivel_cliente)

        st.markdown('<div class="reqflow-project-actions-line"></div>', unsafe_allow_html=True)

        col_espaco, col_botao = st.columns([4.5, 1.6])

        with col_botao:
            if st.button(
                "Abrir requisito",
                key=f"abrir_requisito_{requisito['id']}",
                use_container_width=True
            ):
                st.session_state["requisito_selecionado"] = requisito["id"]
                st.session_state["pagina_atual"] = "Perfil Requisito"
                st.rerun()


def exibir_lista_requisitos(requisitos, funcao):
    if not requisitos:
        st.info("Nenhum requisito encontrado com os filtros selecionados.")
        return

    for requisito in requisitos:
        exibir_card_requisito(requisito, funcao)


def exibir_resumo_quantitativo(requisitos):
    total = len(requisitos)

    em_analise = len([
        requisito for requisito in requisitos
        if requisito["status"] == "em_analise"
    ])

    aguardando = len([
        requisito for requisito in requisitos
        if requisito["status"] == "aguardando_aprovacao"
    ])

    aprovados = len([
        requisito for requisito in requisitos
        if requisito["status"] == "aprovado"
    ])

    reprovados = len([
        requisito for requisito in requisitos
        if requisito["status"] == "reprovado"
    ])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Requisitos", total)

    with col2:
        st.metric("Em análise", em_analise)

    with col3:
        st.metric("Aguardando aprovação", aguardando)

    with col4:
        st.metric("Aprovados/Reprovados", aprovados + reprovados)


def pagina_requisitos():
    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    exibir_topo_requisitos()

    if funcao in ["gerente", "analista"]:
        formulario_cadastro_requisito(id_usuario)
        st.divider()

    if funcao == "cliente":
        requisitos = requisito_controller.listar_cliente(id_usuario)
    else:
        requisitos = requisito_controller.listar_todos()

    requisitos = normalizar_requisitos(requisitos, funcao)

    exibir_resumo_quantitativo(requisitos)

    st.divider()

    texto_busca, tipo_filtro, status_filtro, visibilidade_filtro = exibir_area_filtros(
        requisitos,
        funcao
    )

    if not st.session_state.get("consulta_requisitos_realizada", False):
        st.info("Utilize os filtros acima e clique em **Consultar requisitos** para visualizar os resultados.")
        return

    requisitos_filtrados = aplicar_filtros_requisitos(
        requisitos,
        texto_busca,
        tipo_filtro,
        status_filtro,
        visibilidade_filtro
    )

    st.caption(f"Total encontrado: {len(requisitos_filtrados)} requisito(s).")

    exibir_lista_requisitos(requisitos_filtrados, funcao)