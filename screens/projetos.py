import streamlit as st

from controllers.usuario_controller import UsuarioController
from controllers.projeto_controller import ProjetoController
from controllers.historico_controller import HistoricoController

from components.tabela_projetos import tabela_projetos


def obter_id_usuario_logado():
    return (
        st.session_state.get("id_usuario")
        or st.session_state.get("usuario_id")
        or st.session_state.get("id")
    )


def pagina_projetos():
    usuario_controller = UsuarioController()
    projeto_controller = ProjetoController()
    historico_controller = HistoricoController()

    funcao = st.session_state.get("funcao")

    if "form_projeto_id" not in st.session_state:
        st.session_state["form_projeto_id"] = 0

    mensagem_projeto = st.session_state.pop("mensagem_projeto", None)
    if mensagem_projeto:
        st.success(mensagem_projeto)

    if funcao in ["analista", "gerente"]:
        st.subheader("Cadastrar Projeto")

        clientes = usuario_controller.listar_clientes()
        responsaveis = usuario_controller.listar_responsaveis_projeto()

        if not clientes:
            st.warning(
                "Nenhum cliente cadastrado. "
                "Cadastre um cliente antes de criar um projeto."
            )

        elif not responsaveis:
            st.warning(
                "Nenhum responsável cadastrado. "
                "Cadastre um gerente ou analista antes de criar um projeto."
            )

        else:
            form_id = st.session_state["form_projeto_id"]

            with st.form(
                f"form_cadastro_projeto_{form_id}",
                clear_on_submit=True
            ):
                cliente_selecionado = st.selectbox(
                    "Cliente",
                    options=[None] + clientes,
                    index=0,
                    format_func=lambda x: "Selecione um cliente" if x is None else x[1],
                    key=f"cliente_projeto_{form_id}"
                )

                responsavel_selecionado = st.selectbox(
                    "Responsável pelo Projeto",
                    options=[None] + responsaveis,
                    index=0,
                    format_func=lambda x: (
                        "Selecione um responsável"
                        if x is None
                        else f"{x[1]} - {x[3]}"
                    ),
                    key=f"responsavel_projeto_{form_id}"
                )

                nome = st.text_input(
                    "Nome do Projeto",
                    key=f"nome_projeto_{form_id}"
                )

                descricao = st.text_area(
                    "Descrição",
                    key=f"descricao_projeto_{form_id}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    data_inicio = st.date_input(
                        "Data de Início",
                        value=None,
                        key=f"data_inicio_projeto_{form_id}"
                    )

                with col2:
                    data_fim_prevista = st.date_input(
                        "Data de Término Prevista",
                        value=None,
                        key=f"data_fim_projeto_{form_id}"
                    )

                salvar = st.form_submit_button("Salvar Projeto")

                if salvar:
                    sucesso, resultado = projeto_controller.criar(
                        nome=nome,
                        descricao=descricao,
                        data_inicio=data_inicio,
                        data_fim_prevista=data_fim_prevista,
                        id_responsavel=responsavel_selecionado[0] if responsavel_selecionado else None,
                        id_cliente=cliente_selecionado[0] if cliente_selecionado else None
                    )

                    if not sucesso:
                        st.error(resultado)
                    else:
                        id_projeto = resultado
                        id_usuario_logado = obter_id_usuario_logado()

                        historico_controller.registrar(
                            tipo_entidade="projeto",
                            id_entidade=id_projeto,
                            id_usuario=id_usuario_logado,
                            acao="Projeto criado",
                            descricao=(
                                f"Projeto '{nome.strip()}' criado. "
                                f"Cliente: {cliente_selecionado[1]}. "
                                f"Responsável: {responsavel_selecionado[1]}."
                            )
                        )

                        st.session_state["mensagem_projeto"] = (
                            "Projeto cadastrado com sucesso."
                        )

                        st.session_state["form_projeto_id"] += 1
                        st.rerun()

        st.divider()

    st.subheader("Projetos")
    tabela_projetos()