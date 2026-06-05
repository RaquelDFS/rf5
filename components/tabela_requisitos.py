import streamlit as st

from controllers.requisito_controller import RequisitoController


def formatar_status(status):
    status_formatado = {
        "em_analise": "📝 Em análise",
        "aguardando_aprovacao": "⏳ Aguardando aprovação",
        "aprovado": "✅ Aprovado",
        "reprovado": "❌ Reprovado"
    }

    return status_formatado.get(status, status)


def formatar_tipo(tipo):
    tipo_formatado = {
        "funcional": "Funcional",
        "nao_funcional": "Não funcional"
    }

    return tipo_formatado.get(tipo, tipo)


def tabela_requisitos():
    requisito_controller = RequisitoController()

    st.title("Requisitos")
    st.divider()

    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    if funcao == "cliente":
        requisitos = requisito_controller.listar_cliente(id_usuario)
    else:
        requisitos = requisito_controller.listar_todos()

    if not requisitos:
        st.info("Nenhum requisito encontrado.")
        return

    if funcao == "cliente":
        st.write("Requisitos disponíveis para sua análise.")

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

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
            id_requisito = requisito[0]
            nome = requisito[1]
            tipo = requisito[3]
            status = requisito[4]

            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                st.write(nome)
            with col2:
                st.write(formatar_tipo(tipo))
            with col3:
                st.write(formatar_status(status))
            with col4:
                if st.button("Abrir", key=f"abrir_req_cliente_{id_requisito}"):
                    st.session_state["requisito_selecionado"] = id_requisito
                    st.session_state["pagina_atual"] = "Perfil Requisito"
                    st.rerun()

            st.divider()

    else:
        st.write("Lista geral de requisitos cadastrados no sistema.")

        col1, col2, col3, col4, col5, col6, col7 = st.columns(
            [3, 2, 2, 3, 3, 2, 1]
        )

        with col1:
            st.markdown("**Nome**")
        with col2:
            st.markdown("**Tipo**")
        with col3:
            st.markdown("**Status**")
        with col4:
            st.markdown("**Projeto**")
        with col5:
            st.markdown("**Cliente**")
        with col6:
            st.markdown("**Visível**")
        with col7:
            st.markdown("**Ação**")

        st.divider()

        for requisito in requisitos:
            id_requisito = requisito[0]
            nome = requisito[1]
            tipo = requisito[3]
            status = requisito[4]
            visivel_cliente = requisito[5]
            projeto = requisito[6]
            cliente = requisito[7]

            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [3, 2, 2, 3, 3, 2, 1]
            )

            with col1:
                st.write(nome)
            with col2:
                st.write(formatar_tipo(tipo))
            with col3:
                st.write(formatar_status(status))
            with col4:
                st.write(projeto)
            with col5:
                st.write(cliente)
            with col6:
                st.write("Sim" if visivel_cliente else "Não")
            with col7:
                if st.button("Abrir", key=f"abrir_req_{id_requisito}"):
                    st.session_state["requisito_selecionado"] = id_requisito
                    st.session_state["pagina_atual"] = "Perfil Requisito"
                    st.rerun()

            st.divider()
