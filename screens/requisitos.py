import streamlit as st

from controllers.projeto_controller import ProjetoController
from controllers.requisito_controller import RequisitoController
from controllers.historico_controller import HistoricoController

from components.tabela_requisitos import tabela_requisitos


def pagina_requisitos():
    projeto_controller = ProjetoController()
    requisito_controller = RequisitoController()
    historico_controller = HistoricoController()

    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    if "form_requisito_id" not in st.session_state:
        st.session_state["form_requisito_id"] = 0

    mensagem_requisito = st.session_state.pop("mensagem_requisito", None)
    if mensagem_requisito:
        st.success(mensagem_requisito)

    if funcao in ["analista", "gerente"]:
        st.subheader("Cadastrar Requisito")

        projetos = projeto_controller.listar_por_usuario(id_usuario)

        if not projetos:
            st.warning(
                "Nenhum projeto encontrado. "
                "Cadastre um projeto antes de criar requisitos."
            )
        else:
            form_id = st.session_state["form_requisito_id"]

            with st.form(
                f"form_cadastro_requisito_{form_id}",
                clear_on_submit=True
            ):
                projeto_selecionado = st.selectbox(
                    "Projeto",
                    options=[None] + projetos,
                    index=0,
                    format_func=lambda x: "Selecione um projeto" if x is None else x[1],
                    key=f"projeto_requisito_{form_id}"
                )

                nome = st.text_input(
                    "Nome",
                    key=f"nome_requisito_{form_id}"
                )

                descricao = st.text_area(
                    "Descrição",
                    key=f"descricao_requisito_{form_id}"
                )

                tipo = st.selectbox(
                    "Tipo",
                    options=[None, "funcional", "nao_funcional"],
                    index=0,
                    format_func=lambda x: "Selecione o tipo" if x is None else x,
                    key=f"tipo_requisito_{form_id}"
                )

                visivel_cliente = st.checkbox(
                    "Enviar para aprovação do cliente?",
                    value=False,
                    key=f"visivel_cliente_requisito_{form_id}"
                )

                salvar = st.form_submit_button("Salvar Requisito")

                if salvar:
                    sucesso, resultado = requisito_controller.criar(
                        projeto_id=projeto_selecionado[0] if projeto_selecionado else None,
                        nome=nome,
                        descricao=descricao,
                        tipo=tipo if tipo else "",
                        enviar_para_cliente=visivel_cliente
                    )

                    if not sucesso:
                        st.error(resultado)
                    else:
                        id_requisito = resultado
                        status_inicial = (
                            "aguardando_aprovacao"
                            if visivel_cliente
                            else "em_analise"
                        )

                        historico_controller.registrar(
                            tipo_entidade="requisito",
                            id_entidade=id_requisito,
                            id_usuario=id_usuario,
                            acao="Requisito criado",
                            descricao=(
                                f"Requisito '{nome}' criado no projeto "
                                f"'{projeto_selecionado[1]}' com status "
                                f"'{status_inicial}'."
                            )
                        )

                        st.session_state["mensagem_requisito"] = (
                            "Requisito cadastrado com sucesso."
                        )

                        st.session_state["form_requisito_id"] += 1
                        st.rerun()

        st.divider()

    tabela_requisitos()
import streamlit as st

from database.db import (
    listar_projetos_por_usuario,
    criar_requisito,
    listar_todos_requisitos,
    listar_requisitos_cliente
)


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
            if texto_busca in requisito["nome"].lower()
            or texto_busca in requisito["descricao"].lower()
            or texto_busca in requisito["tipo"].lower()
            or texto_busca in requisito["status"].lower()
            or texto_busca in requisito["projeto"].lower()
            or texto_busca in requisito["cliente"].lower()
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


def exibir_tabela_requisitos(requisitos, funcao):
    if not requisitos:
        st.info("Nenhum requisito encontrado com os filtros selecionados.")
        return

    if funcao == "cliente":
        col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

        with col1:
            st.markdown("**Nome**")
        with col2:
            st.markdown("**Tipo**")
        with col3:
            st.markdown("**Status**")
        with col4:
            st.markdown("**Ação**")

        st.divider()

        for requisito in requisitos:
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.write(requisito["nome"])

            with col2:
                st.write(requisito["tipo"])

            with col3:
                st.write(requisito["status"])

            with col4:
                if st.button("Abrir", key=f"req_cliente_{requisito['id']}"):
                    st.session_state["requisito_selecionado"] = requisito["id"]
                    st.session_state["pagina_atual"] = "Perfil Requisito"
                    st.rerun()

    else:
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])

        with col1:
            st.markdown("**Nome**")
        with col2:
            st.markdown("**Tipo**")
        with col3:
            st.markdown("**Status**")
        with col4:
            st.markdown("**Projeto**")
        with col5:
            st.markdown("**Visível**")
        with col6:
            st.markdown("**Ação**")

        st.divider()

        for requisito in requisitos:
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])

            with col1:
                st.write(requisito["nome"])

            with col2:
                st.write(requisito["tipo"])

            with col3:
                st.write(requisito["status"])

            with col4:
                st.write(requisito["projeto"])

            with col5:
                st.write("Sim" if requisito["visivel_cliente"] else "Não")

            with col6:
                if st.button("Abrir", key=f"req_{requisito['id']}"):
                    st.session_state["requisito_selecionado"] = requisito["id"]
                    st.session_state["pagina_atual"] = "Perfil Requisito"
                    st.rerun()


def formulario_cadastro_requisito(id_usuario):
    st.subheader("Cadastrar Requisito")

    projetos = listar_projetos_por_usuario(id_usuario)

    if not projetos:
        st.warning(
            "Nenhum projeto encontrado. "
            "Cadastre um projeto antes de criar requisitos."
        )
        return

    with st.form("form_cadastro_requisito"):
        projeto_selecionado = st.selectbox(
            "Projeto",
            options=projetos,
            format_func=lambda x: x[1]
        )

        nome = st.text_input("Nome")
        descricao = st.text_area("Descrição")

        tipo = st.selectbox(
            "Tipo",
            ["funcional", "nao_funcional"]
        )

        visivel_cliente = st.checkbox(
            "Enviar para aprovação do cliente?",
            value=True
        )

        salvar = st.form_submit_button("Salvar Requisito")

        if salvar:
            if not nome or not descricao:
                st.error("Preencha o nome e a descrição antes de salvar.")
            else:
                criar_requisito(
                    projeto_id=projeto_selecionado[0],
                    nome=nome,
                    descricao=descricao,
                    tipo=tipo,
                    visivel_cliente=1 if visivel_cliente else 0
                )
                st.success("Requisito cadastrado.")
                st.rerun()


def pagina_requisitos():
    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    st.title("Requisitos")

    if funcao in ["gerente", "analista"]:
        formulario_cadastro_requisito(id_usuario)
        st.divider()

    st.subheader("Consulta de Requisitos")

    if funcao == "cliente":
        requisitos = listar_requisitos_cliente(id_usuario)
    else:
        requisitos = listar_todos_requisitos()

    requisitos = normalizar_requisitos(requisitos, funcao)

    col1, col2 = st.columns([3, 2])

    with col1:
        texto_busca = st.text_input(
            "Buscar requisito",
            placeholder="Digite nome, descrição, tipo, status, projeto ou cliente"
        )

    with col2:
        tipos_disponiveis = sorted(set([requisito["tipo"] for requisito in requisitos]))
        tipo_filtro = st.selectbox(
            "Filtrar por tipo",
            ["Todos"] + tipos_disponiveis
        )

    col3, col4 = st.columns(2)

    with col3:
        status_disponiveis = sorted(set([requisito["status"] for requisito in requisitos]))
        status_filtro = st.selectbox(
            "Filtrar por status",
            ["Todos"] + status_disponiveis
        )

    with col4:
        if funcao == "cliente":
            visibilidade_filtro = "Todos"
            st.selectbox(
                "Visibilidade",
                ["Todos"],
                disabled=True
            )
        else:
            visibilidade_filtro = st.selectbox(
                "Visibilidade",
                [
                    "Todos",
                    "Visível para o cliente",
                    "Não visível para o cliente"
                ]
            )

    requisitos_filtrados = aplicar_filtros_requisitos(
        requisitos,
        texto_busca,
        tipo_filtro,
        status_filtro,
        visibilidade_filtro
    )

    st.caption(f"Total encontrado: {len(requisitos_filtrados)} requisito(s).")

    exibir_tabela_requisitos(requisitos_filtrados, funcao)