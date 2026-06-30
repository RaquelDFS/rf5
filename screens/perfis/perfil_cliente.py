import streamlit as st

from controllers.usuario_controller import UsuarioController
from controllers.requisito_controller import RequisitoController


def formatar_status(status):
    status_formatado = {
        "em_analise": "Em análise",
        "aguardando_aprovacao": "Aguardando aprovação",
        "aprovado": "Aprovado",
        "reprovado": "Reprovado"
    }

    return status_formatado.get(status, status)


def pagina_perfil_cliente():

    usuario_controller = UsuarioController()
    requisito_controller = RequisitoController()

    if "cliente_selecionado" not in st.session_state:
        st.warning("Nenhum cliente selecionado.")
        return

    cliente = usuario_controller.buscar_cliente_por_id(
        st.session_state["cliente_selecionado"]
    )

    if not cliente:
        st.error("Cliente não encontrado.")
        return

    nome_cliente = cliente[1]
    funcao_cliente = cliente[3]
    email_cliente = cliente[4]
    empresa_cliente = cliente[5]
    tipo_cliente = cliente[6]
    documento_cliente = cliente[7]

    st.title("Perfil do Cliente")

    st.write(f"**Contato:** {nome_cliente}")

    if empresa_cliente:
        st.write(f"**Empresa:** {empresa_cliente}")

    if email_cliente:
        st.write(f"**E-mail:** {email_cliente}")

    if tipo_cliente:
        st.write(f"**Tipo de cliente:** {tipo_cliente}")

    if documento_cliente:
        st.write(f"**Documento:** {documento_cliente}")

    st.write(f"**Função:** {funcao_cliente}")

    st.divider()

    st.subheader("Requisitos Associados")

    requisitos = requisito_controller.listar_cliente(cliente[0])

    if not requisitos:
        st.info("Este cliente não possui requisitos cadastrados.")
    else:
        dados = []

        for requisito in requisitos:
            dados.append({
                "Projeto": requisito[5],
                "Requisito": requisito[1],
                "Status": formatar_status(requisito[4])
            })

        st.dataframe(
            dados,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    if st.button("← Voltar para Clientes"):
        st.session_state["pagina_atual"] = "Clientes"
        st.rerun()