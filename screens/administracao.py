import streamlit as st

from database.db import gerar_backup_banco, listar_backups_banco


def pagina_administracao():
    st.title("Administração do Sistema")

    funcao = st.session_state.get("funcao")

    if funcao != "gerente":
        st.warning("Você não possui permissão para acessar a administração do sistema.")
        return

    st.write(
        "Área destinada às rotinas administrativas do ReqFlow, "
        "como geração de backup do banco de dados e apoio à manutenção do sistema."
    )

    st.divider()

    st.subheader("Backup do Banco de Dados")

    st.info(
        "O backup cria uma cópia do arquivo sistema.db dentro da pasta backups. "
        "Essa rotina ajuda a proteger os dados cadastrados no sistema."
    )

    if st.button("Gerar backup do banco de dados", type="primary"):
        sucesso, caminho_backup, mensagem = gerar_backup_banco()

        if sucesso:
            st.success(mensagem)
            st.write(f"Arquivo gerado: `{caminho_backup}`")
        else:
            st.error(mensagem)

    st.divider()

    st.subheader("Backups disponíveis")

    backups = listar_backups_banco()

    if not backups:
        st.warning("Nenhum backup encontrado até o momento.")
    else:
        for backup in backups:
            with st.container():
                st.write(f"**{backup.name}**")
                st.caption(f"Caminho: {backup}")

                with open(backup, "rb") as arquivo:
                    st.download_button(
                        label="Baixar backup",
                        data=arquivo,
                        file_name=backup.name,
                        mime="application/octet-stream",
                        key=f"download_{backup.name}"
                    )

                st.divider()

    st.subheader("Observação sobre restauração")

    st.warning(
        "A restauração do banco deve ser feita manualmente pelo administrador, "
        "com a aplicação desligada. Isso evita conflitos de gravação no SQLite."
    )