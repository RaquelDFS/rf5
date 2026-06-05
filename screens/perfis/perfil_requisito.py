import streamlit as st

from controllers.requisito_controller import RequisitoController
from controllers.comentario_controller import ComentarioController
from controllers.historico_controller import HistoricoController


def buscar_requisito_por_id(id_requisito):
    return RequisitoController().buscar_registro_por_id(id_requisito)


def atualizar_requisito(id_requisito, nome, descricao, tipo, status, visivel_cliente):
    return RequisitoController().atualizar(
        id_requisito=id_requisito,
        nome=nome,
        descricao=descricao,
        tipo=tipo,
        status=status,
        visivel_cliente=visivel_cliente
    )


def excluir_requisito(id_requisito):
    return RequisitoController().excluir(id_requisito)


def criar_comentario_requisito(id_requisito, id_usuario, comentario):
    return ComentarioController().criar(id_requisito, id_usuario, comentario)


def listar_comentarios_requisito(id_requisito):
    return ComentarioController().listar_por_requisito(id_requisito)


def registrar_historico(tipo_entidade, id_entidade, id_usuario, acao, descricao):
    return HistoricoController().registrar(
        tipo_entidade=tipo_entidade,
        id_entidade=id_entidade,
        id_usuario=id_usuario,
        acao=acao,
        descricao=descricao
    )


def listar_historico_requisito(id_requisito):
    return HistoricoController().listar_requisito(id_requisito)


def bloco_comentarios(id_requisito, permitir_novo_comentario=True):
    comentarios = listar_comentarios_requisito(id_requisito)

    if comentarios:
        for comentario in comentarios:
            st.markdown(
                f"**{comentario[3]} ({comentario[4]})** - {comentario[2]}"
            )
            st.write(comentario[1])
            st.divider()
    else:
        st.info("Nenhum comentário registrado para este requisito.")

    if permitir_novo_comentario:
        novo_comentario = st.text_area(
            "Adicionar comentário",
            key=f"comentario_requisito_{id_requisito}"
        )

        if st.button("Enviar Comentário", key=f"btn_comentario_{id_requisito}"):
            if not novo_comentario.strip():
                st.error("Digite um comentário antes de enviar.")
            else:
                criar_comentario_requisito(
                    id_requisito=id_requisito,
                    id_usuario=st.session_state.get("id_usuario"),
                    comentario=novo_comentario
                )

                registrar_historico(
                    tipo_entidade="requisito",
                    id_entidade=id_requisito,
                    id_usuario=st.session_state.get("id_usuario"),
                    acao="Comentário adicionado",
                    descricao="Um novo comentário foi registrado no requisito."
                )

                st.success("Comentário registrado com sucesso.")
                st.rerun()
    else:
        st.info("Novos comentários não estão disponíveis para este status.")


def bloco_historico(id_requisito):
    historicos = listar_historico_requisito(id_requisito)

    if historicos:
        for historico in historicos:
            nome_usuario = historico[4] if historico[4] else "Usuário não identificado"
            funcao_usuario = historico[5] if historico[5] else "sem função"

            st.markdown(
                f"**{historico[1]}** - {historico[3]}"
            )
            st.write(historico[2])
            st.caption(f"Registrado por: {nome_usuario} ({funcao_usuario})")
            st.divider()
    else:
        st.info("Nenhum histórico registrado para este requisito.")


def pagina_perfil_requisito():

    if "requisito_selecionado" not in st.session_state:
        st.warning("Nenhum requisito selecionado.")
        return

    requisito = buscar_requisito_por_id(
        st.session_state["requisito_selecionado"]
    )

    if not requisito:
        st.error("Requisito não encontrado.")
        return

    funcao = st.session_state.get("funcao")
    id_usuario = st.session_state.get("id_usuario")

    st.title("Perfil do Requisito")
    st.divider()

    aba_dados, aba_comentarios, aba_historico = st.tabs(
        [
            "Dados do Requisito",
            "Comentários",
            "Histórico / Rastreabilidade"
        ]
    )

    # ============================================================
    # VISÃO DO CLIENTE
    # ============================================================
    if funcao == "cliente":

        status_atual = requisito[4]
        pode_interagir = status_atual == "aguardando_aprovacao"

        with aba_dados:
            st.subheader("Dados do Requisito")

            st.text_input(
                "Nome",
                value=requisito[1],
                disabled=True
            )

            st.text_area(
                "Descrição",
                value=requisito[2],
                disabled=True
            )

            st.text_input(
                "Tipo",
                value=requisito[3],
                disabled=True
            )

            st.write(f"**Status atual:** {status_atual}")

            st.divider()
            st.subheader("Homologação do Requisito")

            if status_atual == "aguardando_aprovacao":
                st.info(
                    "Este requisito está aguardando sua avaliação. "
                    "Você pode aprovar ou reprovar com justificativa."
                )

                justificativa_reprovacao = st.text_area(
                    "Justificativa da reprovação",
                    key=f"justificativa_reprovacao_{requisito[0]}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Aprovar"):
                        atualizar_requisito(
                            requisito[0],
                            requisito[1],
                            requisito[2],
                            requisito[3],
                            "aprovado",
                            1
                        )

                        criar_comentario_requisito(
                            id_requisito=requisito[0],
                            id_usuario=id_usuario,
                            comentario="Requisito aprovado pelo cliente."
                        )

                        registrar_historico(
                            tipo_entidade="requisito",
                            id_entidade=requisito[0],
                            id_usuario=id_usuario,
                            acao="Requisito aprovado",
                            descricao="O requisito foi aprovado pelo cliente."
                        )

                        st.success("Requisito aprovado.")
                        st.rerun()

                with col2:
                    if st.button("Reprovar"):
                        if not justificativa_reprovacao.strip():
                            st.error(
                                "Informe uma justificativa antes de reprovar o requisito."
                            )
                        else:
                            atualizar_requisito(
                                requisito[0],
                                requisito[1],
                                requisito[2],
                                requisito[3],
                                "reprovado",
                                1
                            )

                            criar_comentario_requisito(
                                id_requisito=requisito[0],
                                id_usuario=id_usuario,
                                comentario=(
                                    "Requisito reprovado pelo cliente. "
                                    f"Justificativa: {justificativa_reprovacao}"
                                )
                            )

                            registrar_historico(
                                tipo_entidade="requisito",
                                id_entidade=requisito[0],
                                id_usuario=id_usuario,
                                acao="Requisito reprovado",
                                descricao=(
                                    "O requisito foi reprovado pelo cliente. "
                                    f"Justificativa: {justificativa_reprovacao}"
                                )
                            )

                            st.success("Requisito reprovado.")
                            st.rerun()

                with col3:
                    if st.button("Voltar"):
                        st.session_state["pagina_atual"] = "Requisitos"
                        st.rerun()

            else:
                if status_atual == "aprovado":
                    st.success("Este requisito já foi aprovado.")
                elif status_atual == "reprovado":
                    st.warning("Este requisito foi reprovado e aguarda ajustes da equipe.")
                else:
                    st.info(
                        "Este requisito ainda não está disponível para aprovação."
                    )

                if st.button("Voltar"):
                    st.session_state["pagina_atual"] = "Requisitos"
                    st.rerun()

        with aba_comentarios:
            st.subheader("Comentários do Requisito")

            bloco_comentarios(
                requisito[0],
                permitir_novo_comentario=pode_interagir
            )

        with aba_historico:
            st.subheader("Histórico / Rastreabilidade")

            bloco_historico(requisito[0])

    # ============================================================
    # VISÃO DOS DEMAIS PERFIS
    # gerente, analista, desenvolvedor, testador
    # ============================================================
    else:

        with aba_dados:
            st.subheader("Dados do Requisito")

            status_atual = requisito[4]

            pode_editar_conteudo = status_atual in [
                "em_analise",
                "reprovado"
            ]

            if not pode_editar_conteudo:
                st.info(
                    "Nome, descrição e tipo ficam bloqueados quando o requisito "
                    "está aguardando aprovação ou já foi aprovado."
                )

            nome = st.text_input(
                "Nome",
                value=requisito[1],
                disabled=not pode_editar_conteudo
            )

            descricao = st.text_area(
                "Descrição",
                value=requisito[2],
                disabled=not pode_editar_conteudo
            )

            tipo = st.selectbox(
                "Tipo",
                ["funcional", "nao_funcional"],
                index=0 if requisito[3] == "funcional" else 1,
                disabled=not pode_editar_conteudo
            )

            opcoes_status = [
                "em_analise",
                "aguardando_aprovacao",
                "aprovado",
                "reprovado"
            ]

            status = st.selectbox(
                "Status",
                opcoes_status,
                index=opcoes_status.index(requisito[4])
            )

            visivel = st.checkbox(
                "Visível para o cliente",
                value=bool(requisito[5])
            )

            st.text_input(
                "Cliente",
                value=requisito[8],
                disabled=True
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Salvar"):
                    alteracoes = []

                    if nome != requisito[1]:
                        alteracoes.append("nome")

                    if descricao != requisito[2]:
                        alteracoes.append("descrição")

                    if tipo != requisito[3]:
                        alteracoes.append("tipo")

                    if status != requisito[4]:
                        alteracoes.append("status")

                    if bool(visivel) != bool(requisito[5]):
                        alteracoes.append("visibilidade para cliente")

                    atualizar_requisito(
                        requisito[0],
                        nome,
                        descricao,
                        tipo,
                        status,
                        1 if visivel else 0
                    )

                    if alteracoes:
                        descricao_historico = (
                            "Requisito atualizado. Campos alterados: "
                            + ", ".join(alteracoes)
                            + "."
                        )
                    else:
                        descricao_historico = (
                            "Botão salvar acionado, mas nenhuma alteração foi identificada."
                        )

                    registrar_historico(
                        tipo_entidade="requisito",
                        id_entidade=requisito[0],
                        id_usuario=id_usuario,
                        acao="Requisito atualizado",
                        descricao=descricao_historico
                    )

                    st.success("Requisito atualizado.")
                    st.rerun()

            with col2:
                if st.button("Excluir"):
                    registrar_historico(
                        tipo_entidade="requisito",
                        id_entidade=requisito[0],
                        id_usuario=id_usuario,
                        acao="Requisito excluído",
                        descricao=f"O requisito '{requisito[1]}' foi excluído."
                    )

                    excluir_requisito(requisito[0])
                    st.session_state["pagina_atual"] = "Requisitos"
                    st.rerun()

            with col3:
                if st.button("Voltar"):
                    st.session_state["pagina_atual"] = "Requisitos"
                    st.rerun()

        with aba_comentarios:
            st.subheader("Comentários do Requisito")

            bloco_comentarios(
                requisito[0],
                permitir_novo_comentario=True
            )

        with aba_historico:
            st.subheader("Histórico / Rastreabilidade")

            bloco_historico(requisito[0])