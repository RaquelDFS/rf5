import streamlit as st

from database.db import listar_requisitos_cliente


def card_modulo(titulo, texto, icone):
    st.markdown(
        f"""
        <div style="
            background: #ffffff;
            border: 1px solid #dbeafe;
            border-radius: 18px;
            padding: 20px;
            min-height: 155px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        ">
            <div style="
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: #eff6ff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
                margin-bottom: 14px;
            ">
                {icone}
            </div>
            <div style="
                font-size: 18px;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 8px;
            ">
                {titulo}
            </div>
            <div style="
                font-size: 14px;
                color: #475569;
                line-height: 1.45;
            ">
                {texto}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_topo_apresentacao(titulo_area, descricao_area):
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            border-radius: 24px;
            padding: 34px 36px;
            margin-bottom: 26px;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.16);
        ">
            <div style="
                display: inline-block;
                background: rgba(255,255,255,0.14);
                color: #dbeafe;
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 16px;
            ">
                Gestão inteligente de requisitos
            </div>
            <div style="
                font-size: 38px;
                font-weight: 900;
                color: #ffffff;
                margin-bottom: 8px;
                letter-spacing: -0.8px;
            ">
                ReqFlow
            </div>
            <div style="
                font-size: 16px;
                color: #dbeafe;
                max-width: 760px;
                line-height: 1.55;
            ">
                Plataforma colaborativa para levantamento, organização, validação
                e documentação de requisitos em projetos de software.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="margin-bottom: 18px;">
            <h2 style="
                color: #0f172a;
                margin-bottom: 6px;
                font-size: 26px;
            ">
                {titulo_area}
            </h2>
            <p style="
                color: #475569;
                font-size: 15px;
                margin-top: 0;
            ">
                {descricao_area}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_cards_apresentacao():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card_modulo(
            "Projetos",
            "Controle dos projetos cadastrados, responsáveis, clientes vinculados e status geral.",
            "📁"
        )

    with col2:
        card_modulo(
            "Requisitos",
            "Registro, organização e acompanhamento dos requisitos funcionais e não funcionais.",
            "📌"
        )

    with col3:
        card_modulo(
            "Clientes",
            "Acompanhamento dos clientes vinculados aos projetos e suas validações.",
            "🤝"
        )

    with col4:
        card_modulo(
            "Validação",
            "Fluxo de aprovação, reprovação, comentários e formalização dos requisitos.",
            "✅"
        )


def exibir_atalhos(titulo, atalhos):
    st.markdown(
        f"""
        <div style="margin-top: 30px; margin-bottom: 12px;">
            <h3 style="
                color: #0f172a;
                font-size: 22px;
                margin-bottom: 4px;
            ">
                {titulo}
            </h3>
            <p style="
                color: #64748b;
                font-size: 14px;
                margin-top: 0;
            ">
                Acesse as principais áreas pelo menu lateral conforme sua permissão.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    colunas = st.columns(len(atalhos))

    for coluna, atalho in zip(colunas, atalhos):
        with coluna:
            st.markdown(
                f"""
                <div style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 16px;
                    padding: 16px;
                    min-height: 110px;
                ">
                    <div style="
                        font-size: 15px;
                        font-weight: 800;
                        color: #0f172a;
                        margin-bottom: 6px;
                    ">
                        {atalho["titulo"]}
                    </div>
                    <div style="
                        font-size: 13px;
                        color: #64748b;
                        line-height: 1.45;
                    ">
                        {atalho["texto"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def inicio_gerente():
    exibir_topo_apresentacao(
        "Visão geral do gerente",
        "Acompanhe os módulos principais do sistema e administre projetos, requisitos, clientes, usuários e rotinas operacionais."
    )

    exibir_cards_apresentacao()

    exibir_atalhos(
        "Áreas principais",
        [
            {
                "titulo": "Gestão de Projetos",
                "texto": "Cadastre, acompanhe e organize os projetos da plataforma."
            },
            {
                "titulo": "Gestão de Usuários",
                "texto": "Crie, edite, ative ou desative usuários do sistema."
            },
            {
                "titulo": "Administração",
                "texto": "Execute rotinas administrativas, como backup do banco de dados."
            }
        ]
    )


def inicio_analista():
    exibir_topo_apresentacao(
        "Área do analista",
        "Organize projetos, cadastre requisitos e acompanhe o fluxo de validação junto ao cliente."
    )

    exibir_cards_apresentacao()

    exibir_atalhos(
        "Atividades do analista",
        [
            {
                "titulo": "Projetos",
                "texto": "Acesse os projetos vinculados e acompanhe o andamento."
            },
            {
                "titulo": "Requisitos",
                "texto": "Cadastre, revise e envie requisitos para validação."
            },
            {
                "titulo": "Clientes",
                "texto": "Consulte os clientes relacionados aos projetos."
            }
        ]
    )


def inicio_desenvolvedor():
    exibir_topo_apresentacao(
        "Área do desenvolvedor",
        "Consulte os projetos e requisitos vinculados para apoiar a execução técnica da solução."
    )

    exibir_cards_apresentacao()

    exibir_atalhos(
        "Atividades do desenvolvedor",
        [
            {
                "titulo": "Projetos",
                "texto": "Visualize os projetos em que está envolvido."
            },
            {
                "titulo": "Requisitos",
                "texto": "Consulte requisitos aprovados ou em desenvolvimento."
            },
            {
                "titulo": "Meu Perfil",
                "texto": "Acesse e atualize seus dados de usuário."
            }
        ]
    )


def inicio_testador():
    exibir_topo_apresentacao(
        "Área do testador",
        "Consulte requisitos e apoie a validação das entregas antes da conclusão do ciclo."
    )

    exibir_cards_apresentacao()

    exibir_atalhos(
        "Atividades do testador",
        [
            {
                "titulo": "Projetos",
                "texto": "Visualize os projetos vinculados ao seu perfil."
            },
            {
                "titulo": "Requisitos",
                "texto": "Acompanhe requisitos disponíveis para teste e revisão."
            },
            {
                "titulo": "Meu Perfil",
                "texto": "Gerencie seus próprios dados de acesso."
            }
        ]
    )


def inicio_cliente():
    exibir_topo_apresentacao(
        "Portal do cliente",
        "Acompanhe seus projetos e consulte os requisitos enviados para validação."
    )

    exibir_cards_apresentacao()

    requisitos = listar_requisitos_cliente(
        st.session_state["id_usuario"]
    )

    st.markdown(
        """
        <div style="margin-top: 30px; margin-bottom: 12px;">
            <h3 style="
                color: #0f172a;
                font-size: 22px;
                margin-bottom: 4px;
            ">
                Requisitos enviados para validação
            </h3>
            <p style="
                color: #64748b;
                font-size: 14px;
                margin-top: 0;
            ">
                Abaixo aparecem os requisitos disponíveis para acompanhamento pelo cliente.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not requisitos:
        st.info("Nenhum requisito encontrado para validação no momento.")
        return

    for requisito in requisitos:
        with st.container():
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.markdown(f"**{requisito[1]}**")

            with col2:
                st.write(requisito[3])

            with col3:
                st.write(requisito[4])

            with col4:
                if st.button("Abrir", key=f"req_inicio_cliente_{requisito[0]}"):
                    st.session_state["requisito_selecionado"] = requisito[0]
                    st.session_state["pagina_atual"] = "Perfil Requisito"
                    st.rerun()

            st.divider()


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