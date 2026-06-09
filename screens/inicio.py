import streamlit as st

from database.db import listar_requisitos_cliente
from components.tabela_requisitos import tabela_requisitos
from components.tabela_projetos import tabela_projetos


def exibir_cards_apresentacao():
    st.title("ReqFlow")
    st.write(
        "Plataforma colaborativa para levantamento, organização, "
        "validação e documentação de requisitos em projetos de software."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("**Projetos**\n\nControle dos projetos cadastrados e seus responsáveis.")

    with col2:
        st.info("**Requisitos**\n\nRegistro e acompanhamento dos requisitos do sistema.")

    with col3:
        st.info("**Clientes**\n\nVisualização dos clientes vinculados aos projetos.")

    with col4:
        st.info("**Validação**\n\nAcompanhamento da aprovação dos requisitos pelo cliente.")

    st.divider()


def inicio_gerente():
    exibir_cards_apresentacao()

    st.subheader("Visão Geral do Sistema")
    st.write(
        "Nesta área, o gerente pode acompanhar os principais módulos do ReqFlow, "
        "incluindo projetos, requisitos, clientes e usuários."
    )

    st.divider()

    st.subheader("Projetos cadastrados")
    tabela_projetos()

    st.divider()

    st.subheader("Requisitos cadastrados")
    tabela_requisitos()


def inicio_analista():
    exibir_cards_apresentacao()

    st.subheader("Área do Analista")
    st.write(
        "Aqui o analista pode acompanhar seus projetos, cadastrar requisitos "
        "e organizar as informações levantadas junto ao cliente."
    )

    st.divider()

    st.subheader("Meus Projetos")
    tabela_projetos()

    st.divider()

    st.subheader("Requisitos")
    tabela_requisitos()


def inicio_desenvolvedor():
    exibir_cards_apresentacao()

    st.subheader("Área do Desenvolvedor")
    st.write(
        "Aqui o desenvolvedor pode acompanhar os projetos e requisitos vinculados, "
        "consultando as informações necessárias para o desenvolvimento."
    )

    st.divider()

    st.subheader("Projetos vinculados")
    tabela_projetos()

    st.divider()

    st.subheader("Requisitos disponíveis")
    tabela_requisitos()


def inicio_testador():
    exibir_cards_apresentacao()

    st.subheader("Área do Testador")
    st.write(
        "Aqui o testador pode consultar projetos e requisitos para apoiar "
        "a validação das entregas do sistema."
    )

    st.divider()

    st.subheader("Projetos vinculados")
    tabela_projetos()

    st.divider()

    st.subheader("Requisitos disponíveis")
    tabela_requisitos()


def inicio_cliente():
    exibir_cards_apresentacao()

    st.subheader("Portal do Cliente")
    st.write(
        "Aqui o cliente pode acompanhar os requisitos enviados para validação "
        "e consultar as informações dos projetos vinculados."
    )

    requisitos = listar_requisitos_cliente(
        st.session_state["id_usuario"]
    )

    st.divider()
    st.subheader("Meus Requisitos")

    if not requisitos:
        st.info("Nenhum requisito encontrado.")
        return

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
            st.write(requisito[1])

        with col2:
            st.write(requisito[3])

        with col3:
            st.write(requisito[4])

        with col4:
            if st.button("Abrir", key=f"req_inicio_cliente_{requisito[0]}"):
                st.session_state["requisito_selecionado"] = requisito[0]
                st.session_state["pagina_atual"] = "Perfil Requisito"
                st.rerun()


def pagina_inicio():
    funcao = st.session_state.get("funcao")

    if funcao == "gerente":
        inicio_gerente()

    elif funcao == "analista":
        inicio_analista()

    elif funcao == "desenvolvedor":
        inicio_desenvolvedor()

    elif funcao == "testador":
        inicio_testador()

    elif funcao == "cliente":
        inicio_cliente()

    else:
        st.title("ReqFlow")
        st.warning("Perfil de usuário não identificado.")