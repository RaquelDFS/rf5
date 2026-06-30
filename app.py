import streamlit as st

from config.navigation import PAGINAS
from database.db import inicializar_banco
from utils.style import carregar_css
from views.dashboard import tela_dashboard
from views.login import tela_login


st.set_page_config(
    page_title="ReqFlow",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

carregar_css()

inicializar_banco()

if "logado" not in st.session_state:
    st.session_state["logado"] = False


if not st.session_state["logado"]:
    tela_login()
else:
    pagina = tela_dashboard()

    if pagina in PAGINAS:
        PAGINAS[pagina]()
    else:
        st.error("Página não encontrada.")