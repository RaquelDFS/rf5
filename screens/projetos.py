import streamlit as st
from html import escape

from controllers.projeto_controller import ProjetoController
from controllers.usuario_controller import UsuarioController


projeto_controller = ProjetoController()
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


def formatar_status_projeto(status):
    mapa = {
        "iniciado": "Iniciado",
        "em_aprovacao": "Em aprovação",
        "aprovado": "Aprovado",
        "em_construcao": "Em construção",
        "em_atraso": "Em atraso",
        "em_revisao": "Em revisão",
        "concluido": "Concluído",
        "suspenso": "Suspenso",
        "cancelado": "Cancelado"
    }

    return mapa.get(status, texto_seguro(status))


def exibir_topo_projetos():
    st.markdown(
        """
        <div class="reqflow-page-hero">
            <div class="reqflow-page-hero-pill">
                Gestão de projetos
            </div>
            <div class="reqflow-page-hero-title">
                Projetos
            </div>
            <div class="reqflow-page-hero-text">
                Cadastre, acompanhe e organize os projetos vinculados aos clientes,
                responsáveis e requisitos da plataforma ReqFlow.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def inicializar_estado_consulta_projetos():
    if "consulta_projetos_realizada" not in st.session_state:
        st.session_state["consulta_projetos_realizada"] = False


def marcar_consulta_projetos():
    st.session_state["consulta_projetos_realizada"] = True


def limpar_consulta_projetos():
    st.session_state["consulta_projetos_realizada"] = False
    st.session_state["filtro_projetos_texto"] = ""
    st.session_state["filtro_projetos_status"] = "Todos"


def normalizar_projetos(projetos, funcao):
    projetos_normalizados = []

    for projeto in projetos:
        projetos_normalizados.append({
            "id": projeto[0],
            "nome": projeto[1],
            "descricao": projeto[2],
            "status": projeto[3],
            "data_inicio": projeto[4],
            "data_fim_prevista": projeto[5],
            "data_formalizacao": projeto[6],
            "responsavel": projeto[7],
            "cliente": projeto[8]
        })

    return projetos_normalizados


def aplicar_filtros_projetos(projetos, texto_busca, status_filtro):
    resultado = projetos

    if texto_busca:
        texto_busca = texto_busca.lower()

        resultado = [
            projeto for projeto in resultado
            if texto_busca in str(projeto["nome"]).lower()
            or texto_busca in str(projeto["descricao"]).lower()
            or texto_busca in str(projeto["status"]).lower()
            or texto_busca in str(projeto["cliente"]).lower()
            or texto_busca in str(projeto["responsavel"]).lower()
        ]

    if status_filtro != "Todos":
        resultado = [
            projeto for projeto in resultado
            if projeto["status"] == status_filtro
        ]

    return resultado


def classe_status_projeto(status):
    status_texto = str(status).lower()

    if "concluído" in status_texto or "concluido" in status_texto:
        return "reqflow-status-green"

    if "aprovado" in status_texto:
        return "reqflow-status-green"

    if "andamento" in status_texto:
        return "reqflow-status-blue"

    if "construção" in status_texto or "construcao" in status_texto:
        return "reqflow-status-blue"

    if "iniciado" in status_texto:
        return "reqflow-status-blue"

    if "aprovação" in status_texto or "aprovacao" in status_texto:
        return "reqflow-status-yellow"

    if "revisão" in status_texto or "revisao" in status_texto:
        return "reqflow-status-yellow"

    if "pausado" in status_texto or "suspenso" in status_texto:
        return "reqflow-status-yellow"

    if "atraso" in status_texto:
        return "reqflow-status-red"

    if "cancelado" in status_texto or "reprovado" in status_texto:
        return "reqflow-status-red"

    return "reqflow-status-gray"


def exibir_badge_status(status):
    status_formatado = formatar_status_projeto(status)
    classe_status = classe_status_projeto(status_formatado)

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


def exibir_info_projeto(label, valor):
    st.markdown(
        f"""
        <div class="reqflow-project-info-box">
            <div class="reqflow-project-info-label">{texto_html(label)}</div>
            <div class="reqflow-project-info-value">{texto_html(valor)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_card_projeto(projeto):
    nome = texto_seguro(projeto["nome"])
    descricao = texto_seguro(projeto["descricao"])
    status = texto_seguro(projeto["status"])
    cliente = texto_seguro(projeto["cliente"])
    responsavel = texto_seguro(projeto["responsavel"])
    data_inicio = texto_seguro(projeto["data_inicio"])
    data_fim_prevista = texto_seguro(projeto["data_fim_prevista"])

    with st.container(border=True):
        col_titulo, col_status = st.columns([5, 1.4])

        with col_titulo:
            st.markdown(
                f"""
                <div class="reqflow-project-title">
                    {texto_html(nome)}
                </div>
                <div class="reqflow-project-description">
                    {texto_html(descricao)}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_status:
            exibir_badge_status(status)

        st.markdown(
            '<div class="reqflow-project-section-space"></div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            exibir_info_projeto("Cliente", cliente)

        with col2:
            exibir_info_projeto("Responsável", responsavel)

        with col3:
            exibir_info_projeto("Início", data_inicio)

        with col4:
            exibir_info_projeto("Prazo", data_fim_prevista)

        st.markdown(
            '<div class="reqflow-project-actions-line"></div>',
            unsafe_allow_html=True
        )

        col_espaco, col_botao = st.columns([4.5, 1.6])

        with col_botao:
            if st.button(
                "Abrir projeto",
                key=f"proj_{projeto['id']}",
                use_container_width=True
            ):
                st.session_state["projeto_selecionado"] = projeto["id"]
                st.session_state["pagina_atual"] = "Perfil Projeto"
                st.rerun()


def exibir_lista_projetos(projetos):
    if not projetos:
        st.info("Nenhum projeto encontrado com os filtros selecionados.")
        return

    for projeto in projetos:
        exibir_card_projeto(projeto)


def formulario_cadastro_projeto(id_usuario):
    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Novo projeto</h3>
            <p>Preencha as informações abaixo para cadastrar um novo projeto no ReqFlow.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    clientes = usuario_controller.listar_clientes()

    if not clientes:
        st.warning("Nenhum cliente cadastrado. Cadastre um cliente antes de criar um projeto.")
        return

    with st.form("form_cadastro_projeto", clear_on_submit=True):
        cliente_selecionado = st.selectbox(
            "Cliente",
            options=[None] + clientes,
            index=0,
            format_func=lambda x: "Selecione um cliente" if x is None else x[1]
        )

        nome = st.text_input(
            "Nome do Projeto",
            placeholder="Ex.: Plataforma de atendimento interno"
        )

        descricao = st.text_area(
            "Descrição",
            placeholder="Descreva brevemente o objetivo, escopo ou contexto do projeto."
        )

        col1, col2 = st.columns(2)

        with col1:
            data_inicio = st.date_input("Data de Início")

        with col2:
            data_fim_prevista = st.date_input("Data de Término Prevista")

        salvar = st.form_submit_button("Salvar Projeto", use_container_width=True)

        if salvar:
            if cliente_selecionado is None:
                st.error("Selecione um cliente antes de salvar.")
                return

            sucesso, resultado = projeto_controller.criar(
                nome=nome,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim_prevista=data_fim_prevista,
                id_responsavel=id_usuario,
                id_cliente=cliente_selecionado[0]
            )

            if not sucesso:
                st.error(resultado)
                return

            st.success("Projeto cadastrado com sucesso.")
            st.rerun()


def exibir_area_filtros(projetos):
    inicializar_estado_consulta_projetos()

    st.markdown(
        """
        <div class="reqflow-section-title-block">
            <h3>Consulta de projetos</h3>
            <p>Utilize os filtros para localizar projetos por nome, descrição, status, cliente ou responsável.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        texto_busca = st.text_input(
            "Buscar projeto",
            placeholder="Digite nome, descrição, status, cliente ou responsável",
            key="filtro_projetos_texto"
        )

    with col2:
        status_disponiveis = sorted(set([projeto["status"] for projeto in projetos]))

        status_filtro = st.selectbox(
            "Filtrar por status",
            ["Todos"] + status_disponiveis,
            format_func=lambda x: x if x == "Todos" else formatar_status_projeto(x),
            key="filtro_projetos_status"
        )

    col_botao1, col_botao2, col_espaco = st.columns([1.4, 1.4, 4])

    with col_botao1:
        st.button(
            "Consultar projetos",
            type="primary",
            use_container_width=True,
            on_click=marcar_consulta_projetos
        )

    with col_botao2:
        st.button(
            "Limpar consulta",
            use_container_width=True,
            on_click=limpar_consulta_projetos
        )

    return texto_busca, status_filtro


def exibir_resumo_quantitativo(projetos):
    total = len(projetos)

    em_andamento = len([
        projeto for projeto in projetos
        if "andamento" in str(projeto["status"]).lower()
        or "construcao" in str(projeto["status"]).lower()
        or "construção" in str(projeto["status"]).lower()
    ])

    iniciados = len([
        projeto for projeto in projetos
        if "iniciado" in str(projeto["status"]).lower()
    ])

    concluidos = len([
        projeto for projeto in projetos
        if "concluído" in str(projeto["status"]).lower()
        or "concluido" in str(projeto["status"]).lower()
        or "aprovado" in str(projeto["status"]).lower()
    ])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Projetos cadastrados", total)

    with col2:
        st.metric("Iniciados / andamento", iniciados + em_andamento)

    with col3:
        st.metric("Aprovados / concluídos", concluidos)


def pagina_projetos():
    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    exibir_topo_projetos()

    if funcao == "gerente":
        projetos = projeto_controller.listar()
    else:
        projetos = projeto_controller.listar_por_usuario(id_usuario)

    projetos = normalizar_projetos(projetos, funcao)

    exibir_resumo_quantitativo(projetos)

    st.divider()

    if funcao in ["gerente", "analista"]:
        formulario_cadastro_projeto(id_usuario)
        st.divider()

    texto_busca, status_filtro = exibir_area_filtros(projetos)

    if not st.session_state.get("consulta_projetos_realizada", False):
        st.info("Utilize os filtros acima e clique em **Consultar projetos** para visualizar os resultados.")
        return

    projetos_filtrados = aplicar_filtros_projetos(
        projetos,
        texto_busca,
        status_filtro
    )

    st.caption(f"Total encontrado: {len(projetos_filtrados)} projeto(s).")

    exibir_lista_projetos(projetos_filtrados)