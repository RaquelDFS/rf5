import streamlit as st
import datetime
from io import BytesIO

from controllers.projeto_controller import ProjetoController
from controllers.requisito_controller import RequisitoController
from controllers.usuario_controller import UsuarioController
from controllers.historico_controller import HistoricoController

from screens.requisitos import pagina_requisitos


def buscar_projeto_por_id(id_projeto):
    return ProjetoController().buscar_registro_por_id(id_projeto)


def atualizar_projeto(
    id_projeto,
    nome,
    descricao,
    status,
    data_inicio,
    data_fim_prevista,
    id_responsavel,
    id_cliente=None
):
    return ProjetoController().atualizar(
        id_projeto=id_projeto,
        nome=nome,
        descricao=descricao,
        status=status,
        data_inicio=data_inicio,
        data_fim_prevista=data_fim_prevista,
        id_responsavel=id_responsavel,
        id_cliente=id_cliente
    )


def listar_requisitos_por_projeto(id_projeto):
    return RequisitoController().listar_por_projeto(id_projeto)


def listar_responsaveis_projeto():
    return UsuarioController().listar_responsaveis_projeto()


def listar_clientes():
    return UsuarioController().listar_clientes()


def registrar_historico(tipo_entidade, id_entidade, id_usuario, acao, descricao):
    return HistoricoController().registrar(
        tipo_entidade=tipo_entidade,
        id_entidade=id_entidade,
        id_usuario=id_usuario,
        acao=acao,
        descricao=descricao
    )


def listar_historico_projeto(id_projeto):
    return HistoricoController().listar_projeto(id_projeto)


def registrar_formalizacao(id_projeto, data_formalizacao):
    return ProjetoController().registrar_formalizacao(id_projeto, data_formalizacao)


def listar_requisitos_completos_por_projeto(id_projeto):
    return ProjetoController().listar_requisitos_completos(id_projeto)


def listar_comentarios_por_projeto(id_projeto):
    return ProjetoController().listar_comentarios(id_projeto)


def listar_historico_por_projeto_e_requisitos(id_projeto):
    return ProjetoController().listar_historico_completo(id_projeto)


def listar_aprovacoes_reprovacoes_por_projeto(id_projeto):
    return ProjetoController().listar_aprovacoes_reprovacoes(id_projeto)






def obter_id_usuario_logado():
    return (
        st.session_state.get("id_usuario")
        or st.session_state.get("usuario_id")
        or st.session_state.get("id")
    )


def formatar_status(status):
    mapa = {
        "iniciado": "Iniciado",
        "em_aprovacao": "Em aprovação",
        "aprovado": "Aprovado",
        "em_construcao": "Em construção",
        "em_atraso": "Em atraso",
        "em_revisao": "Em revisão",
        "concluido": "Concluído",
        "suspenso": "Suspenso",
        "cancelado": "Cancelado",
        "em_analise": "Em análise",
        "aguardando_aprovacao": "Aguardando aprovação",
        "reprovado": "Reprovado"
    }

    return mapa.get(status, status)


def formatar_tipo(tipo):
    mapa = {
        "funcional": "Funcional",
        "nao_funcional": "Não funcional"
    }

    return mapa.get(tipo, tipo)


def formatar_visibilidade(valor):
    if valor == 1:
        return "Sim"

    return "Não"


def texto_seguro(valor):
    if valor is None:
        return "-"

    texto = str(valor).strip()

    if texto == "":
        return "-"

    return texto


def converter_data_para_input(data_texto):
    if not data_texto:
        return datetime.date.today()

    try:
        return datetime.date.fromisoformat(data_texto)
    except Exception:
        try:
            return datetime.datetime.strptime(data_texto, "%d/%m/%Y").date()
        except Exception:
            return datetime.date.today()


def escrever_linha_pdf(texto, largura_maxima=95):
    texto = texto_seguro(texto)

    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual + " " + palavra) <= largura_maxima:
            linha_atual = (linha_atual + " " + palavra).strip()
        else:
            linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    if not linhas:
        linhas.append("-")

    return linhas


def montar_descricao_alteracoes(
    projeto,
    nome,
    descricao,
    status,
    data_inicio,
    data_fim_prevista,
    responsavel_selecionado,
    cliente_selecionado
):
    alteracoes = []

    if nome != projeto[1]:
        alteracoes.append(
            f"Nome alterado de '{projeto[1]}' para '{nome}'."
        )

    if descricao != projeto[2]:
        alteracoes.append(
            "Descrição do projeto alterada."
        )

    if status != projeto[3]:
        alteracoes.append(
            f"Status alterado de '{formatar_status(projeto[3])}' para '{formatar_status(status)}'."
        )

    if str(data_inicio) != projeto[4]:
        alteracoes.append(
            f"Data de início alterada de '{projeto[4]}' para '{data_inicio}'."
        )

    if str(data_fim_prevista) != projeto[5]:
        alteracoes.append(
            f"Data de término prevista alterada de '{projeto[5]}' para '{data_fim_prevista}'."
        )

    if responsavel_selecionado and responsavel_selecionado[0] != projeto[7]:
        alteracoes.append(
            f"Responsável alterado de '{projeto[9]}' para '{responsavel_selecionado[1]}'."
        )

    if cliente_selecionado and cliente_selecionado[0] != projeto[8]:
        alteracoes.append(
            f"Cliente alterado de '{projeto[10]}' para '{cliente_selecionado[1]}'."
        )

    return alteracoes






def mostrar_historico_projeto(id_projeto):
    historico = listar_historico_projeto(id_projeto)

    if not historico:
        st.info("Nenhum histórico registrado para este projeto.")
        return

    for item in historico:
        acao = item[1]
        descricao = item[2]
        data_historico = item[3]
        nome_usuario = item[4] if item[4] else "Sistema"
        funcao_usuario = item[5] if item[5] else "sem perfil"

        with st.container(border=True):
            st.markdown(f"**{acao}**")
            st.write(descricao)
            st.caption(
                f"Registrado em {data_historico} por {nome_usuario} ({funcao_usuario})"
            )






def mostrar_requisitos_do_projeto(id_projeto):
    st.subheader("Requisitos do Projeto")

    requisitos = listar_requisitos_por_projeto(id_projeto)

    if not requisitos:
        st.info("Nenhum requisito cadastrado neste projeto.")
        return

    for req in requisitos:
        id_requisito = req[0]
        nome = req[1]
        descricao = req[2]
        tipo = req[3]
        status = req[4]
        visivel_cliente = req[5]

        with st.container(border=True):
            st.markdown(f"**#{id_requisito} - {nome}**")
            st.write(f"**Tipo:** {formatar_tipo(tipo)}")
            st.write(f"**Status:** {formatar_status(status)}")
            st.write(f"**Visível ao cliente:** {formatar_visibilidade(visivel_cliente)}")
            st.write(descricao)

            if st.button("Abrir requisito", key=f"abrir_req_projeto_{id_requisito}"):
                st.session_state["requisito_selecionado"] = id_requisito
                st.session_state["pagina_atual"] = "Perfil Requisito"
                st.rerun()






def gerar_pdf_projeto_completo(
    projeto,
    requisitos,
    comentarios,
    historico,
    aprovacoes_reprovacoes
):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
    except ImportError:
        return None, "A biblioteca reportlab não está instalada. Rode: pip install reportlab"

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    margem_esquerda = 2 * cm
    margem_direita = 2 * cm
    posicao_y = altura - 2 * cm

    data_geracao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def nova_pagina_se_necessario(espaco=2 * cm):
        nonlocal posicao_y

        if posicao_y < espaco:
            pdf.showPage()
            posicao_y = altura - 2 * cm

    def escrever_titulo(texto):
        nonlocal posicao_y

        nova_pagina_se_necessario()
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(margem_esquerda, posicao_y, texto)
        posicao_y -= 0.9 * cm

    def escrever_subtitulo(texto):
        nonlocal posicao_y

        nova_pagina_se_necessario()
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(margem_esquerda, posicao_y, texto)
        posicao_y -= 0.65 * cm

    def escrever_texto(texto, fonte="Helvetica", tamanho=10, recuo=0):
        nonlocal posicao_y

        pdf.setFont(fonte, tamanho)

        for linha in escrever_linha_pdf(str(texto)):
            nova_pagina_se_necessario()
            pdf.drawString(margem_esquerda + recuo, posicao_y, linha)
            posicao_y -= 0.45 * cm

    def escrever_espaco(tamanho=0.3):
        nonlocal posicao_y
        posicao_y -= tamanho * cm

    def escrever_linha_horizontal():
        nonlocal posicao_y

        nova_pagina_se_necessario()
        pdf.line(
            margem_esquerda,
            posicao_y,
            largura - margem_direita,
            posicao_y
        )
        posicao_y -= 0.35 * cm




    escrever_titulo("ReqFlow - Documentação Formal do Projeto")

    escrever_texto(
        "Documento gerado automaticamente pela plataforma ReqFlow para formalização, "
        "rastreabilidade e acompanhamento dos requisitos do projeto."
    )

    escrever_espaco(0.4)

    escrever_texto(f"Projeto: {texto_seguro(projeto[1])}", "Helvetica-Bold", 11)
    escrever_texto(f"Cliente: {texto_seguro(projeto[10])}")
    escrever_texto(f"Responsável: {texto_seguro(projeto[9])}")
    escrever_texto(f"Status do projeto: {formatar_status(projeto[3])}")
    escrever_texto(f"Data de geração: {data_geracao}")

    escrever_espaco(0.5)
    escrever_linha_horizontal()




    escrever_subtitulo("1. Dados do Projeto")

    escrever_texto(f"ID do projeto: {projeto[0]}")
    escrever_texto(f"Nome do projeto: {projeto[1]}")
    escrever_texto(f"Descrição: {projeto[2]}")
    escrever_texto(f"Status: {formatar_status(projeto[3])}")
    escrever_texto(f"Data de início: {projeto[4]}")
    escrever_texto(f"Data de término prevista: {projeto[5]}")

    if projeto[6]:
        escrever_texto(f"Data de formalização: {projeto[6]}")
    else:
        escrever_texto("Data de formalização: Ainda não formalizado")

    escrever_texto(f"Responsável: {projeto[9]}")
    escrever_texto(f"Cliente: {projeto[10]}")

    escrever_espaco(0.4)




    escrever_subtitulo("2. Resumo dos Requisitos")

    if not requisitos:
        escrever_texto("Nenhum requisito cadastrado para este projeto.")
    else:
        total_requisitos = len(requisitos)
        total_aprovados = sum(1 for r in requisitos if r["status"] == "aprovado")
        total_reprovados = sum(1 for r in requisitos if r["status"] == "reprovado")
        total_aguardando = sum(1 for r in requisitos if r["status"] == "aguardando_aprovacao")
        total_em_analise = sum(1 for r in requisitos if r["status"] == "em_analise")

        escrever_texto(f"Total de requisitos: {total_requisitos}")
        escrever_texto(f"Requisitos aprovados: {total_aprovados}")
        escrever_texto(f"Requisitos reprovados: {total_reprovados}")
        escrever_texto(f"Requisitos aguardando aprovação: {total_aguardando}")
        escrever_texto(f"Requisitos em análise: {total_em_analise}")

    escrever_espaco(0.4)




    escrever_subtitulo("3. Detalhamento dos Requisitos")

    if not requisitos:
        escrever_texto("Nenhum requisito cadastrado para detalhamento.")
    else:
        for indice, requisito in enumerate(requisitos, start=1):
            nova_pagina_se_necessario(5 * cm)

            escrever_texto(
                f"3.{indice} - Requisito #{requisito['id']}: {requisito['nome']}",
                "Helvetica-Bold",
                11
            )

            escrever_texto(f"Tipo: {formatar_tipo(requisito['tipo'])}", recuo=0.3 * cm)
            escrever_texto(f"Status: {formatar_status(requisito['status'])}", recuo=0.3 * cm)
            escrever_texto(
                f"Visível ao cliente: {formatar_visibilidade(requisito['visivel_cliente'])}",
                recuo=0.3 * cm
            )
            escrever_texto(f"Descrição: {requisito['descricao']}", recuo=0.3 * cm)

            escrever_espaco(0.3)




    escrever_subtitulo("4. Aprovações e Reprovações")

    if not aprovacoes_reprovacoes:
        escrever_texto(
            "Nenhum registro específico de aprovação ou reprovação foi encontrado para este projeto."
        )
    else:
        for item in aprovacoes_reprovacoes:
            nova_pagina_se_necessario(4 * cm)

            escrever_texto(
                f"Requisito: {texto_seguro(item['requisito'])}",
                "Helvetica-Bold",
                10
            )
            escrever_texto(f"Ação: {texto_seguro(item['acao'])}", recuo=0.3 * cm)
            escrever_texto(f"Descrição: {texto_seguro(item['descricao'])}", recuo=0.3 * cm)
            escrever_texto(f"Usuário: {texto_seguro(item['usuario'])} ({texto_seguro(item['funcao'])})", recuo=0.3 * cm)
            escrever_texto(f"Data: {texto_seguro(item['data_historico'])}", recuo=0.3 * cm)

            escrever_espaco(0.25)




    escrever_subtitulo("5. Comentários e Colaboração")

    if not comentarios:
        escrever_texto("Nenhum comentário foi registrado nos requisitos deste projeto.")
    else:
        for comentario in comentarios:
            nova_pagina_se_necessario(4 * cm)

            escrever_texto(
                f"Requisito: {texto_seguro(comentario['requisito'])}",
                "Helvetica-Bold",
                10
            )
            escrever_texto(
                f"Usuário: {texto_seguro(comentario['usuario'])} ({texto_seguro(comentario['funcao'])})",
                recuo=0.3 * cm
            )
            escrever_texto(f"Data: {texto_seguro(comentario['data_comentario'])}", recuo=0.3 * cm)
            escrever_texto(f"Comentário: {texto_seguro(comentario['comentario'])}", recuo=0.3 * cm)

            escrever_espaco(0.25)




    escrever_subtitulo("6. Histórico e Rastreabilidade")

    if not historico:
        escrever_texto("Nenhum histórico de rastreabilidade foi registrado para este projeto.")
    else:
        for item in historico:
            nova_pagina_se_necessario(4 * cm)

            entidade = texto_seguro(item["tipo_entidade"])

            if item["tipo_entidade"] == "requisito" and item["requisito"]:
                entidade = f"Requisito: {item['requisito']}"

            escrever_texto(f"Entidade: {entidade}", "Helvetica-Bold", 10)
            escrever_texto(f"Ação: {texto_seguro(item['acao'])}", recuo=0.3 * cm)
            escrever_texto(f"Descrição: {texto_seguro(item['descricao'])}", recuo=0.3 * cm)
            escrever_texto(
                f"Usuário: {texto_seguro(item['usuario'])} ({texto_seguro(item['funcao'])})",
                recuo=0.3 * cm
            )
            escrever_texto(f"Data: {texto_seguro(item['data_historico'])}", recuo=0.3 * cm)

            escrever_espaco(0.25)




    escrever_subtitulo("7. Formalização")

    escrever_texto(
        "Este documento consolida os dados do projeto, os requisitos cadastrados, "
        "os registros de colaboração, as aprovações, reprovações e o histórico de "
        "rastreabilidade disponível no ReqFlow até o momento de sua geração."
    )

    escrever_texto(
        "A emissão deste PDF registra a formalização da documentação do projeto "
        "dentro do fluxo da plataforma."
    )

    escrever_espaco(0.4)
    escrever_texto(f"Documento gerado automaticamente em {data_geracao}.")

    pdf.save()

    buffer.seek(0)
    return buffer.getvalue(), None






def mostrar_exportacao_pdf(projeto):
    st.subheader("Exportação da Documentação do Projeto")

    st.write(
        "Nesta área é possível gerar um PDF completo com os dados do projeto, "
        "requisitos, comentários, aprovações/reprovações e histórico de rastreabilidade."
    )

    requisitos = listar_requisitos_completos_por_projeto(projeto[0])
    comentarios = listar_comentarios_por_projeto(projeto[0])
    historico = listar_historico_por_projeto_e_requisitos(projeto[0])
    aprovacoes_reprovacoes = listar_aprovacoes_reprovacoes_por_projeto(projeto[0])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Requisitos", len(requisitos))

    with col2:
        st.metric("Comentários", len(comentarios))

    with col3:
        st.metric("Histórico", len(historico))

    with col4:
        st.metric("Aprovações/Reprovações", len(aprovacoes_reprovacoes))

    if not requisitos:
        st.warning(
            "Este projeto ainda não possui requisitos cadastrados. "
            "O PDF poderá ser gerado, mas ficará sem lista de requisitos."
        )

    st.divider()

    nome_arquivo = f"documentacao_projeto_{projeto[0]}.pdf"

    if st.button("Gerar PDF do Projeto"):
        pdf_bytes, erro = gerar_pdf_projeto_completo(
            projeto=projeto,
            requisitos=requisitos,
            comentarios=comentarios,
            historico=historico,
            aprovacoes_reprovacoes=aprovacoes_reprovacoes
        )

        if erro:
            st.error(erro)
            return

        st.session_state[f"pdf_projeto_{projeto[0]}"] = pdf_bytes

        data_formalizacao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        id_usuario_logado = obter_id_usuario_logado()

        registrar_formalizacao(projeto[0], data_formalizacao)

        registrar_historico(
            tipo_entidade="projeto",
            id_entidade=projeto[0],
            id_usuario=id_usuario_logado,
            acao="PDF gerado",
            descricao=(
                f"Documento PDF completo do projeto '{projeto[1]}' gerado em "
                f"{data_formalizacao}, contendo dados do projeto, requisitos, "
                f"comentários, aprovações/reprovações e rastreabilidade."
            )
        )

        st.success("PDF gerado com sucesso.")

    pdf_salvo = st.session_state.get(f"pdf_projeto_{projeto[0]}")

    if pdf_salvo:
        st.download_button(
            label="Baixar PDF",
            data=pdf_salvo,
            file_name=nome_arquivo,
            mime="application/pdf"
        )






def pagina_perfil_projeto():

    if "projeto_selecionado" not in st.session_state:
        st.warning("Nenhum projeto selecionado.")
        return

    projeto = buscar_projeto_por_id(
        st.session_state["projeto_selecionado"]
    )

    if not projeto:
        st.error("Projeto não encontrado.")
        return

    funcao = st.session_state.get("funcao")

    st.title("Perfil do Projeto")
    st.caption(f"Projeto selecionado: {projeto[1]}")
    st.divider()

    aba_dados, aba_requisitos, aba_historico, aba_exportacao = st.tabs([
        "Dados do Projeto",
        "Requisitos",
        "Histórico / Rastreabilidade",
        "Exportação PDF"
    ])




    with aba_dados:




        if funcao == "cliente":
            st.text_input("Nome", value=projeto[1], disabled=True)
            st.text_area("Descrição", value=projeto[2], disabled=True)
            st.text_input("Status", value=formatar_status(projeto[3]), disabled=True)
            st.text_input("Início", value=projeto[4], disabled=True)
            st.text_input("Prazo", value=projeto[5], disabled=True)
            st.text_input("Responsável", value=projeto[9], disabled=True)
            st.text_input("Cliente", value=projeto[10], disabled=True)

            if projeto[6]:
                st.text_input(
                    "Formalizado em",
                    value=projeto[6],
                    disabled=True
                )

            if st.button("Voltar"):
                st.session_state["pagina_atual"] = "Projetos"
                st.rerun()




        elif funcao in ["analista", "gerente"]:

            nome = st.text_input("Nome", value=projeto[1])
            descricao = st.text_area("Descrição", value=projeto[2])

            lista_status = [
                "iniciado",
                "em_aprovacao",
                "aprovado",
                "em_construcao",
                "em_atraso",
                "em_revisao",
                "concluido",
                "suspenso",
                "cancelado"
            ]

            status = st.selectbox(
                "Status",
                lista_status,
                index=lista_status.index(projeto[3]) if projeto[3] in lista_status else 0,
                format_func=formatar_status
            )

            data_inicio = st.date_input(
                "Início",
                value=converter_data_para_input(projeto[4])
            )

            data_fim_prevista = st.date_input(
                "Prazo",
                value=converter_data_para_input(projeto[5])
            )




            if funcao == "gerente":
                responsaveis = listar_responsaveis_projeto()
                clientes = listar_clientes()

                if not responsaveis:
                    st.warning("Nenhum responsável ativo encontrado.")
                    responsavel_selecionado = None
                else:
                    responsavel_selecionado = st.selectbox(
                        "Responsável",
                        options=responsaveis,
                        index=next(
                            (
                                i for i, r in enumerate(responsaveis)
                                if r[0] == projeto[7]
                            ),
                            0
                        ),
                        format_func=lambda x: f"{x[1]} - {x[3]}"
                    )

                if not clientes:
                    st.warning("Nenhum cliente ativo encontrado.")
                    cliente_selecionado = None
                else:
                    cliente_selecionado = st.selectbox(
                        "Cliente",
                        options=clientes,
                        index=next(
                            (
                                i for i, c in enumerate(clientes)
                                if c[0] == projeto[8]
                            ),
                            0
                        ),
                        format_func=lambda x: x[1]
                    )

            else:
                responsavel_selecionado = None
                cliente_selecionado = None

                st.text_input("Responsável", value=projeto[9], disabled=True)
                st.text_input("Cliente", value=projeto[10], disabled=True)

            if projeto[6]:
                st.text_input(
                    "Formalizado em",
                    value=projeto[6],
                    disabled=True
                )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Salvar"):

                    if not nome.strip() or not descricao.strip():
                        st.error("Preencha o nome e a descrição antes de salvar.")

                    else:
                        if funcao == "gerente":
                            if responsavel_selecionado is None:
                                st.error("Selecione um responsável antes de salvar.")
                                return

                            if cliente_selecionado is None:
                                st.error("Selecione um cliente antes de salvar.")
                                return

                            id_responsavel = responsavel_selecionado[0]
                            id_cliente = cliente_selecionado[0]

                        else:
                            id_responsavel = projeto[7]
                            id_cliente = projeto[8]

                        alteracoes = montar_descricao_alteracoes(
                            projeto=projeto,
                            nome=nome.strip(),
                            descricao=descricao.strip(),
                            status=status,
                            data_inicio=data_inicio,
                            data_fim_prevista=data_fim_prevista,
                            responsavel_selecionado=responsavel_selecionado,
                            cliente_selecionado=cliente_selecionado
                        )

                        atualizar_projeto(
                            projeto[0],
                            nome.strip(),
                            descricao.strip(),
                            status,
                            str(data_inicio),
                            str(data_fim_prevista),
                            id_responsavel,
                            id_cliente
                        )

                        if alteracoes:
                            id_usuario_logado = obter_id_usuario_logado()

                            registrar_historico(
                                tipo_entidade="projeto",
                                id_entidade=projeto[0],
                                id_usuario=id_usuario_logado,
                                acao="Projeto atualizado",
                                descricao=" ".join(alteracoes)
                            )

                        st.success("Projeto atualizado.")
                        st.rerun()

            with col2:
                if st.button("Voltar"):
                    st.session_state["pagina_atual"] = "Projetos"
                    st.rerun()




        else:
            st.warning("Você não possui permissão para acessar este perfil de projeto.")




    with aba_requisitos:
        if funcao in ["analista", "gerente"]:
            st.info(
                "Abaixo é possível visualizar os requisitos vinculados ao projeto. "
                "Para cadastrar novos requisitos, utilize a tela de Requisitos no menu principal."
            )

        mostrar_requisitos_do_projeto(projeto[0])




    with aba_historico:
        st.subheader("Histórico / Rastreabilidade do Projeto")
        mostrar_historico_projeto(projeto[0])




    with aba_exportacao:
        if funcao in ["analista", "gerente"]:
            mostrar_exportacao_pdf(projeto)
        else:
            st.warning("Você não possui permissão para gerar documentação do projeto.")