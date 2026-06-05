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
