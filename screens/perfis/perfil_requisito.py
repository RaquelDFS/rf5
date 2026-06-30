import html
import streamlit as st
from textwrap import dedent

from controllers.requisito_controller import RequisitoController
from controllers.comentario_controller import ComentarioController
from controllers.historico_controller import HistoricoController


requisito_controller = RequisitoController()
comentario_controller = ComentarioController()
historico_controller = HistoricoController()


def buscar_requisito_por_id(id_requisito):
    return requisito_controller.buscar_registro_por_id(id_requisito)


def atualizar_requisito(id_requisito, nome, descricao, tipo, status, visivel_cliente):
    return requisito_controller.atualizar(
        id_requisito=id_requisito,
        nome=nome,
        descricao=descricao,
        tipo=tipo,
        status=status,
        visivel_cliente=visivel_cliente
    )


def excluir_requisito(id_requisito):
    return requisito_controller.excluir(id_requisito)


def criar_comentario_requisito(id_requisito, id_usuario, comentario):
    return comentario_controller.criar(id_requisito, id_usuario, comentario)


def listar_comentarios_requisito(id_requisito):
    return comentario_controller.listar_por_requisito(id_requisito)


def registrar_historico(tipo_entidade, id_entidade, id_usuario, acao, descricao):
    return historico_controller.registrar(
        tipo_entidade=tipo_entidade,
        id_entidade=id_entidade,
        id_usuario=id_usuario,
        acao=acao,
        descricao=descricao
    )


def listar_historico_requisito(id_requisito):
    return historico_controller.listar_requisito(id_requisito)


def texto_seguro(valor):
    if valor is None:
        return "-"

    texto = str(valor).strip()

    if texto == "":
        return "-"

    return texto


def texto_html(valor):
    return html.escape(texto_seguro(valor))


def formatar_status(status):
    mapa = {
        "em_analise": "Em análise",
        "aguardando_aprovacao": "Aguardando aprovação",
        "aprovado": "Aprovado",
        "reprovado": "Reprovado"
    }

    return mapa.get(status, texto_seguro(status))


def formatar_tipo(tipo):
    mapa = {
        "funcional": "Funcional",
        "nao_funcional": "Não funcional"
    }

    return mapa.get(tipo, texto_seguro(tipo))


def formatar_visibilidade(valor):
    if valor == 1 or valor is True:
        return "Sim"

    return "Não"


def formatar_codigo_requisito(id_requisito):
    return f"REQ-{int(id_requisito):03d}"


def classe_status_requisito(status):
    status_texto = texto_seguro(status).lower()

    if "aprovado" in status_texto:
        return "reqflow-status-green"

    if "aguardando" in status_texto:
        return "reqflow-status-yellow"

    if "reprovado" in status_texto:
        return "reqflow-status-red"

    if "analise" in status_texto or "análise" in status_texto:
        return "reqflow-status-blue"

    return "reqflow-status-gray"


def obter_indice_status(status_atual, opcoes_status):
    if status_atual in opcoes_status:
        return opcoes_status.index(status_atual)

    return 0


def exibir_estilos_perfil_requisito():
    st.markdown(
        dedent(
            """
            <style>
                .reqflow-requisito-hero {
                    background: linear-gradient(135deg, #061B3A 0%, #0B6BFF 100%);
                    border-radius: 24px;
                    padding: 30px 34px;
                    margin-bottom: 24px;
                    box-shadow: 0 16px 38px rgba(6, 27, 58, 0.18);
                    position: relative;
                    overflow: hidden;
                }

                .reqflow-requisito-hero::before {
                    content: "";
                    position: absolute;
                    width: 380px;
                    height: 380px;
                    right: -160px;
                    top: -180px;
                    background: rgba(255, 255, 255, 0.10);
                    border-radius: 50%;
                }

                .reqflow-requisito-hero::after {
                    content: "";
                    position: absolute;
                    width: 280px;
                    height: 280px;
                    left: -120px;
                    bottom: -150px;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 50%;
                }

                .reqflow-requisito-hero-content {
                    position: relative;
                    z-index: 2;
                }

                .reqflow-requisito-pill {
                    display: inline-block;
                    background: rgba(255, 255, 255, 0.14);
                    color: #DBEAFE !important;
                    padding: 6px 12px;
                    border-radius: 999px;
                    font-size: 13px;
                    font-weight: 800;
                    margin-bottom: 14px;
                }

                .reqflow-requisito-title-row {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    gap: 20px;
                    margin-bottom: 22px;
                }

                .reqflow-requisito-title {
                    font-size: 34px;
                    line-height: 1.15;
                    font-weight: 900;
                    color: #FFFFFF !important;
                    letter-spacing: -0.7px;
                    margin-bottom: 8px;
                }

                .reqflow-requisito-description {
                    font-size: 15px;
                    line-height: 1.55;
                    color: #DCEBFF !important;
                    max-width: 850px;
                }

                .reqflow-requisito-grid {
                    display: grid;
                    grid-template-columns: repeat(4, minmax(0, 1fr));
                    gap: 14px;
                    margin-top: 18px;
                }

                .reqflow-requisito-grid-item {
                    background: rgba(255, 255, 255, 0.13);
                    border: 1px solid rgba(255, 255, 255, 0.22);
                    border-radius: 16px;
                    padding: 13px 15px;
                    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
                }

                .reqflow-requisito-grid-item span {
                    display: block;
                    color: #BFDBFE !important;
                    font-size: 11px;
                    font-weight: 900;
                    text-transform: uppercase;
                    letter-spacing: 0.45px;
                    margin-bottom: 5px;
                }

                .reqflow-requisito-grid-item strong {
                    display: block;
                    color: #FFFFFF !important;
                    font-size: 14px;
                    font-weight: 850;
                    line-height: 1.35;
                }

                .reqflow-validacao-card {
                    background: #FFFFFF;
                    border: 1.5px solid #B8D4FA;
                    border-left: 6px solid #0B6BFF;
                    border-radius: 18px;
                    padding: 20px 22px;
                    margin-bottom: 18px;
                    box-shadow: 0 12px 28px rgba(6, 27, 58, 0.10);
                }

                .reqflow-validacao-card h3 {
                    color: #061B3A !important;
                    font-size: 21px;
                    font-weight: 900;
                    margin-bottom: 6px;
                }

                .reqflow-validacao-card p {
                    color: #60758C !important;
                    font-size: 14px;
                    line-height: 1.55;
                    margin-bottom: 0;
                }

                .reqflow-info-grid {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 14px;
                    margin-bottom: 20px;
                }

                .reqflow-info-card {
                    background: linear-gradient(180deg, #F8FBFF 0%, #EEF6FF 100%);
                    border: 1.5px solid #B8D4FA;
                    border-top: 4px solid #0B6BFF;
                    border-radius: 14px;
                    padding: 12px 14px;
                    min-height: 78px;
                    box-shadow: 0 8px 18px rgba(6, 27, 58, 0.07);
                }

                .reqflow-info-card-label {
                    font-size: 11px;
                    color: #0B6BFF !important;
                    font-weight: 900;
                    text-transform: uppercase;
                    letter-spacing: 0.45px;
                    margin-bottom: 6px;
                }

                .reqflow-info-card-value {
                    font-size: 14px;
                    color: #102A43 !important;
                    font-weight: 850;
                    line-height: 1.35;
                }

                .reqflow-descricao-card {
                    background: #FFFFFF;
                    border: 1.5px solid #D9E6F7;
                    border-radius: 18px;
                    padding: 18px 20px;
                    margin-bottom: 18px;
                    box-shadow: 0 10px 24px rgba(6, 27, 58, 0.07);
                }

                .reqflow-descricao-card h4 {
                    color: #061B3A !important;
                    font-size: 18px;
                    font-weight: 900;
                    margin-bottom: 8px;
                }

                .reqflow-descricao-card p {
                    color: #102A43 !important;
                    font-size: 14px;
                    line-height: 1.65;
                    margin-bottom: 0;
                }

                .reqflow-decisao-alerta {
                    background: #FFF7E6;
                    border: 1.5px solid #FCD34D;
                    border-left: 6px solid #F59E0B;
                    border-radius: 16px;
                    padding: 16px 18px;
                    margin-bottom: 18px;
                    box-shadow: 0 10px 24px rgba(245, 158, 11, 0.10);
                }

                .reqflow-decisao-alerta strong {
                    color: #92400E !important;
                    display: block;
                    font-size: 15px;
                    margin-bottom: 4px;
                }

                .reqflow-decisao-alerta span {
                    color: #78350F !important;
                    font-size: 14px;
                    line-height: 1.5;
                }

                @media (max-width: 900px) {
                    .reqflow-requisito-title-row {
                        flex-direction: column;
                    }

                    .reqflow-requisito-grid,
                    .reqflow-info-grid {
                        grid-template-columns: 1fr;
                    }

                    .reqflow-requisito-title {
                        font-size: 28px;
                    }
                }
            </style>
            """
        ),
        unsafe_allow_html=True
    )


def exibir_status_badge(status):
    status_formatado = formatar_status(status)
    classe_status = classe_status_requisito(status_formatado)

    st.markdown(
        dedent(
            f"""
            <span class="reqflow-project-status {classe_status}">
                {texto_html(status_formatado)}
            </span>
            """
        ),
        unsafe_allow_html=True
    )


def exibir_topo_perfil_requisito(requisito):
    id_requisito = requisito[0]
    nome = texto_html(requisito[1])
    descricao = texto_html(requisito[2])
    tipo = texto_html(formatar_tipo(requisito[3]))
    status = texto_html(formatar_status(requisito[4]))
    cliente = texto_html(requisito[8])
    codigo_requisito = texto_html(formatar_codigo_requisito(id_requisito))
    classe_status = classe_status_requisito(status)

    st.markdown(
        dedent(
            f"""
            <div class="reqflow-requisito-hero">
                <div class="reqflow-requisito-hero-content">
                    <div class="reqflow-requisito-pill">Perfil do requisito</div>

                    <div class="reqflow-requisito-title-row">
                        <div>
                            <div class="reqflow-requisito-title">{nome}</div>
                            <div class="reqflow-requisito-description">{descricao}</div>
                        </div>

                        <div>
                            <span class="reqflow-project-status {classe_status}">
                                {status}
                            </span>
                        </div>
                    </div>

                    <div class="reqflow-requisito-grid">
                        <div class="reqflow-requisito-grid-item">
                            <span>Código</span>
                            <strong>{codigo_requisito}</strong>
                        </div>

                        <div class="reqflow-requisito-grid-item">
                            <span>Status</span>
                            <strong>{status}</strong>
                        </div>

                        <div class="reqflow-requisito-grid-item">
                            <span>Cliente</span>
                            <strong>{cliente}</strong>
                        </div>

                        <div class="reqflow-requisito-grid-item">
                            <span>Tipo</span>
                            <strong>{tipo}</strong>
                        </div>
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )


def exibir_titulo_secao(titulo, descricao):
    st.markdown(
        dedent(
            f"""
            <div class="reqflow-section-title-block">
                <h3>{texto_html(titulo)}</h3>
                <p>{texto_html(descricao)}</p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )


def exibir_card_info(label, valor):
    st.markdown(
        dedent(
            f"""
            <div class="reqflow-info-card">
                <div class="reqflow-info-card-label">{texto_html(label)}</div>
                <div class="reqflow-info-card-value">{texto_html(valor)}</div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )


def exibir_resumo_requisito(requisito):
    st.markdown('<div class="reqflow-info-grid">', unsafe_allow_html=True)

    exibir_card_info("Código", formatar_codigo_requisito(requisito[0]))
    exibir_card_info("Projeto", f"Projeto #{requisito[6]}")
    exibir_card_info("Cliente", requisito[8])
    exibir_card_info("Tipo", formatar_tipo(requisito[3]))
    exibir_card_info("Status", formatar_status(requisito[4]))
    exibir_card_info("Visível ao cliente", formatar_visibilidade(requisito[5]))

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        dedent(
            f"""
            <div class="reqflow-descricao-card">
                <h4>Descrição do requisito</h4>
                <p>{texto_html(requisito[2])}</p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )


def montar_descricao_alteracoes(requisito, nome, descricao, tipo, status, visivel):
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

    if alteracoes:
        return "Requisito atualizado. Campos alterados: " + ", ".join(alteracoes) + "."

    return "Botão salvar acionado, mas nenhuma alteração foi identificada."


def bloco_comentarios(id_requisito, permitir_novo_comentario=True):
    exibir_titulo_secao(
        "Comentários do requisito",
        "Registre observações, dúvidas, decisões e alinhamentos relacionados ao requisito."
    )

    comentarios = listar_comentarios_requisito(id_requisito)

    if comentarios:
        for comentario in comentarios:
            texto_comentario = texto_html(comentario[1])
            data_comentario = texto_html(comentario[2])
            nome_usuario = texto_html(comentario[3])
            funcao_usuario = texto_html(comentario[4])

            st.markdown(
                dedent(
                    f"""
                    <div class="reqflow-comment-card">
                        <div class="reqflow-comment-header">
                            {nome_usuario} <span>({funcao_usuario})</span>
                        </div>
                        <div class="reqflow-comment-text">
                            {texto_comentario}
                        </div>
                        <div class="reqflow-comment-footer">
                            Registrado em {data_comentario}
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )
    else:
        st.info("Nenhum comentário registrado para este requisito.")

    if permitir_novo_comentario:
        st.markdown(
            dedent(
                """
                <div class="reqflow-validacao-card">
                    <h3>Novo comentário</h3>
                    <p>Use este campo para registrar dúvidas, ajustes combinados ou observações antes da decisão final.</p>
                </div>
                """
            ),
            unsafe_allow_html=True
        )

        novo_comentario = st.text_area(
            "Adicionar comentário",
            key=f"comentario_requisito_{id_requisito}"
        )

        col_espaco, col_botao = st.columns([4, 1.6])

        with col_botao:
            if st.button(
                "Enviar comentário",
                key=f"btn_comentario_{id_requisito}",
                use_container_width=True
            ):
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
            acao = texto_html(historico[1])
            descricao = texto_html(historico[2])
            data_historico = texto_html(historico[3])
            nome_usuario = texto_html(historico[4] if historico[4] else "Usuário não identificado")
            funcao_usuario = texto_html(historico[5] if historico[5] else "sem função")

            st.markdown(
                dedent(
                    f"""
                    <div class="reqflow-history-card">
                        <div class="reqflow-history-title">{acao}</div>
                        <div class="reqflow-history-description">{descricao}</div>
                        <div class="reqflow-history-footer">
                            Registrado em {data_historico} por {nome_usuario} ({funcao_usuario})
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )
    else:
        st.info("Nenhum histórico registrado para este requisito.")


def aprovar_requisito_cliente(requisito, id_usuario):
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


def reprovar_requisito_cliente(requisito, id_usuario, justificativa):
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
            f"Justificativa: {justificativa}"
        )
    )

    registrar_historico(
        tipo_entidade="requisito",
        id_entidade=requisito[0],
        id_usuario=id_usuario,
        acao="Requisito reprovado",
        descricao=(
            "O requisito foi reprovado pelo cliente. "
            f"Justificativa: {justificativa}"
        )
    )


def mostrar_dados_cliente(requisito, id_usuario):
    status_atual = requisito[4]

    exibir_titulo_secao(
        "Validação do cliente",
        "Confira os dados do requisito e registre a decisão formal de aprovação ou reprovação."
    )

    exibir_resumo_requisito(requisito)

    if status_atual == "aguardando_aprovacao":
        st.markdown(
            dedent(
                """
                <div class="reqflow-decisao-alerta">
                    <strong>Este requisito está aguardando avaliação.</strong>
                    <span>Antes de aprovar ou reprovar, revise a descrição e use os comentários caso precise registrar alguma dúvida ou alinhamento.</span>
                </div>
                """
            ),
            unsafe_allow_html=True
        )

        justificativa_reprovacao = st.text_area(
            "Justificativa para reprovação ou solicitação de ajuste",
            key=f"justificativa_reprovacao_{requisito[0]}"
        )

        col_aprovar, col_reprovar, col_voltar = st.columns(3)

        with col_aprovar:
            if st.button("Aprovar requisito", use_container_width=True):
                aprovar_requisito_cliente(requisito, id_usuario)
                st.success("Requisito aprovado.")
                st.rerun()

        with col_reprovar:
            if st.button("Reprovar / solicitar ajuste", use_container_width=True):
                if not justificativa_reprovacao.strip():
                    st.error("Informe uma justificativa antes de reprovar ou solicitar ajuste.")
                else:
                    reprovar_requisito_cliente(
                        requisito,
                        id_usuario,
                        justificativa_reprovacao
                    )
                    st.success("Requisito reprovado com justificativa registrada.")
                    st.rerun()

        with col_voltar:
            if st.button("Voltar", use_container_width=True):
                st.session_state["pagina_atual"] = "Requisitos"
                st.rerun()
    else:
        if status_atual == "aprovado":
            st.success("Este requisito já foi aprovado.")
        elif status_atual == "reprovado":
            st.warning("Este requisito foi reprovado e aguarda ajustes da equipe.")
        else:
            st.info("Este requisito ainda não está disponível para aprovação.")

        if st.button("Voltar", use_container_width=True):
            st.session_state["pagina_atual"] = "Requisitos"
            st.rerun()


def mostrar_dados_equipe(requisito, id_usuario):
    status_atual = requisito[4]
    pode_editar_conteudo = status_atual in ["em_analise", "reprovado"]

    exibir_titulo_secao(
        "Gestão do requisito",
        "Altere as informações necessárias e salve para registrar a atualização no histórico."
    )

    exibir_resumo_requisito(requisito)

    if not pode_editar_conteudo:
        st.info(
            "Este requisito está em uma etapa controlada. "
            "Por isso, nome, descrição e tipo estão bloqueados para edição."
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

    col_tipo, col_status = st.columns(2)

    with col_tipo:
        tipo = st.selectbox(
            "Tipo",
            ["funcional", "nao_funcional"],
            index=0 if requisito[3] == "funcional" else 1,
            disabled=not pode_editar_conteudo,
            format_func=formatar_tipo
        )

    with col_status:
        opcoes_status = [
            "em_analise",
            "aguardando_aprovacao",
            "aprovado",
            "reprovado"
        ]

        status = st.selectbox(
            "Status",
            opcoes_status,
            index=obter_indice_status(requisito[4], opcoes_status),
            format_func=formatar_status
        )

    col_cliente, col_visivel = st.columns(2)

    with col_cliente:
        st.text_input(
            "Cliente",
            value=requisito[8],
            disabled=True
        )

    with col_visivel:
        visivel = st.checkbox(
            "Visível para o cliente",
            value=bool(requisito[5])
        )

    st.markdown(
        '<div class="reqflow-project-actions-line"></div>',
        unsafe_allow_html=True
    )

    col_salvar, col_excluir, col_voltar = st.columns(3)

    with col_salvar:
        if st.button("Salvar alterações", use_container_width=True):
            descricao_historico = montar_descricao_alteracoes(
                requisito=requisito,
                nome=nome,
                descricao=descricao,
                tipo=tipo,
                status=status,
                visivel=visivel
            )

            atualizar_requisito(
                requisito[0],
                nome,
                descricao,
                tipo,
                status,
                1 if visivel else 0
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

    with col_excluir:
        if st.button(
            "Excluir requisito",
            use_container_width=True,
            disabled=not pode_editar_conteudo
        ):
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

    with col_voltar:
        if st.button("Voltar", use_container_width=True):
            st.session_state["pagina_atual"] = "Requisitos"
            st.rerun()


def pagina_perfil_requisito():
    exibir_estilos_perfil_requisito()

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

    exibir_topo_perfil_requisito(requisito)

    aba_dados, aba_comentarios, aba_historico = st.tabs(
        [
            "Dados e Validação",
            "Comentários",
            "Histórico / Rastreabilidade"
        ]
    )

    if funcao == "cliente":
        pode_interagir = requisito[4] == "aguardando_aprovacao"

        with aba_dados:
            mostrar_dados_cliente(requisito, id_usuario)

        with aba_comentarios:
            bloco_comentarios(
                requisito[0],
                permitir_novo_comentario=pode_interagir
            )

        with aba_historico:
            exibir_titulo_secao(
                "Histórico / Rastreabilidade",
                "Acompanhe as principais alterações registradas neste requisito."
            )
            bloco_historico(requisito[0])
    else:
        with aba_dados:
            mostrar_dados_equipe(requisito, id_usuario)

        with aba_comentarios:
            bloco_comentarios(
                requisito[0],
                permitir_novo_comentario=True
            )

        with aba_historico:
            exibir_titulo_secao(
                "Histórico / Rastreabilidade",
                "Acompanhe as principais alterações registradas neste requisito."
            )
            bloco_historico(requisito[0])