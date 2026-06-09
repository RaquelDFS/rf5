import streamlit as st

from database.db import (
    listar_clientes,
    criar_projeto,
    listar_projetos,
    listar_projetos_por_usuario
)


def normalizar_projetos(projetos, funcao):
    projetos_normalizados = []

    for projeto in projetos:
        if funcao == "gerente":
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
        else:
            projetos_normalizados.append({
                "id": projeto[0],
                "nome": projeto[1],
                "descricao": projeto[2],
                "status": projeto[3],
                "data_inicio": projeto[4],
                "data_fim_prevista": projeto[5],
                "data_formalizacao": "",
                "responsavel": "",
                "cliente": ""
            })

    return projetos_normalizados


def aplicar_filtros_projetos(projetos, texto_busca, status_filtro):
    resultado = projetos

    if texto_busca:
        texto_busca = texto_busca.lower()

        resultado = [
            projeto for projeto in resultado
            if texto_busca in projeto["nome"].lower()
            or texto_busca in projeto["descricao"].lower()
            or texto_busca in projeto["status"].lower()
            or texto_busca in projeto["cliente"].lower()
            or texto_busca in projeto["responsavel"].lower()
        ]

    if status_filtro != "Todos":
        resultado = [
            projeto for projeto in resultado
            if projeto["status"] == status_filtro
        ]

    return resultado


def exibir_tabela_projetos(projetos):
    if not projetos:
        st.info("Nenhum projeto encontrado com os filtros selecionados.")
        return

    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

    with col1:
        st.markdown("**Nome**")
    with col2:
        st.markdown("**Status**")
    with col3:
        st.markdown("**Início**")
    with col4:
        st.markdown("**Prazo**")
    with col5:
        st.markdown("**Ação**")

    st.divider()

    for projeto in projetos:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

        with col1:
            st.write(projeto["nome"])

        with col2:
            st.write(projeto["status"])

        with col3:
            st.write(projeto["data_inicio"])

        with col4:
            st.write(projeto["data_fim_prevista"])

        with col5:
            if st.button("Abrir", key=f"proj_{projeto['id']}"):
                st.session_state["projeto_selecionado"] = projeto["id"]
                st.session_state["pagina_atual"] = "Perfil Projeto"
                st.rerun()


def formulario_cadastro_projeto(id_usuario):
    st.subheader("Cadastrar Projeto")

    clientes = listar_clientes()

    if not clientes:
        st.warning("Nenhum cliente cadastrado. Cadastre um cliente antes de criar um projeto.")
        return

    with st.form("form_cadastro_projeto"):
        cliente_selecionado = st.selectbox(
            "Cliente",
            options=clientes,
            format_func=lambda x: x[1]
        )

        nome = st.text_input("Nome do Projeto")
        descricao = st.text_area("Descrição")

        col1, col2 = st.columns(2)

        with col1:
            data_inicio = st.date_input("Data de Início")

        with col2:
            data_fim_prevista = st.date_input("Data de Término Prevista")

        salvar = st.form_submit_button("Salvar Projeto")

        if salvar:
            if not nome or not descricao:
                st.error("Preencha todos os campos antes de salvar.")
            else:
                criar_projeto(
                    nome,
                    descricao,
                    str(data_inicio),
                    str(data_fim_prevista),
                    id_responsavel=id_usuario,
                    id_cliente=cliente_selecionado[0]
                )
                st.success("Projeto cadastrado.")
                st.rerun()


def pagina_projetos():
    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    st.title("Projetos")

    if funcao in ["gerente", "analista"]:
        formulario_cadastro_projeto(id_usuario)
        st.divider()

    st.subheader("Consulta de Projetos")

    if funcao == "gerente":
        projetos = listar_projetos()
    else:
        projetos = listar_projetos_por_usuario(id_usuario)

    projetos = normalizar_projetos(projetos, funcao)

    col1, col2 = st.columns([3, 2])

    with col1:
        texto_busca = st.text_input(
            "Buscar projeto",
            placeholder="Digite nome, descrição, status, cliente ou responsável"
        )

    with col2:
        status_disponiveis = sorted(set([projeto["status"] for projeto in projetos]))
        status_filtro = st.selectbox(
            "Filtrar por status",
            ["Todos"] + status_disponiveis
        )

    projetos_filtrados = aplicar_filtros_projetos(
        projetos,
        texto_busca,
        status_filtro
    )

    st.caption(f"Total encontrado: {len(projetos_filtrados)} projeto(s).")

    exibir_tabela_projetos(projetos_filtrados)