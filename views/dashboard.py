import streamlit as st
from pathlib import Path

from config.navigation import MENUS


def exibir_logo_sidebar():
    caminho_logo = Path("assets/logo_reqflow_horizontal.png")

    st.sidebar.markdown(
        """
        <div style="
            padding: 18px 6px 8px 6px;
            text-align: center;
            margin-bottom: 8px;
        ">
        """,
        unsafe_allow_html=True
    )

    if caminho_logo.exists():
        st.sidebar.image(
            str(caminho_logo),
            use_container_width=True
        )
    else:
        st.sidebar.markdown(
            """
            <div style="
                font-size: 28px;
                font-weight: 900;
                color: #ffffff;
                letter-spacing: -0.4px;
            ">
                ReqFlow
            </div>
            """,
            unsafe_allow_html=True
        )

    st.sidebar.markdown(
        """
            <div style="
                font-size: 12px;
                color: rgba(255,255,255,0.72);
                margin-top: 4px;
                line-height: 1.35;
                text-align: center;
            ">
                Gestão de requisitos
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_usuario_sidebar(usuario, funcao):
    funcao_formatada = str(funcao).replace("_", " ").title()

    st.sidebar.markdown(
        f"""
        <div style="
            padding: 12px 12px 14px 12px;
            margin: 10px 0 14px 0;
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 14px;
            background: rgba(255,255,255,0.06);
            box-shadow: 0 8px 18px rgba(0,0,0,0.14);
        ">
            <div style="
                font-size: 12px;
                color: rgba(255,255,255,0.55);
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.7px;
                margin-bottom: 6px;
            ">
                Usuário logado
            </div>
            <div style="
                font-size: 14px;
                font-weight: 800;
                color: #FFFFFF;
                line-height: 1.35;
                word-break: break-word;
            ">
                {usuario}
            </div>
            <div style="
                display: inline-block;
                font-size: 11px;
                font-weight: 800;
                color: #DBEAFE;
                background: rgba(11,107,255,0.28);
                border: 1px solid rgba(147,197,253,0.35);
                border-radius: 999px;
                padding: 4px 9px;
                margin-top: 8px;
            ">
                {funcao_formatada}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def exibir_titulo_navegacao():
    st.sidebar.markdown(
        """
        <div style="
            font-size: 11px;
            font-weight: 800;
            color: rgba(255,255,255,0.56);
            text-transform: uppercase;
            letter-spacing: 0.9px;
            margin: 12px 0 8px 2px;
        ">
            Navegação
        </div>
        """,
        unsafe_allow_html=True
    )


def sair_do_sistema():
    st.session_state.clear()
    st.query_params.clear()
    st.rerun()


def tela_dashboard():
    usuario = st.session_state.get("usuario", "Usuário")
    funcao = st.session_state.get("funcao", "")

    menus_usuario = MENUS.get(funcao, ["Início"])

    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = menus_usuario[0]

    pagina_atual = st.session_state["pagina_atual"]

    exibir_logo_sidebar()
    exibir_usuario_sidebar(usuario, funcao)
    exibir_titulo_navegacao()

    for item in menus_usuario:
        rotulo = f"▸ {item}" if item == pagina_atual else item

        if st.sidebar.button(
            rotulo,
            use_container_width=True,
            key=f"menu_{item}"
        ):
            st.session_state["pagina_atual"] = item
            st.rerun()

    st.sidebar.divider()

    if st.sidebar.button(
        "Sair",
        use_container_width=True,
        key="botao_sair"
    ):
        sair_do_sistema()

    return st.session_state["pagina_atual"]