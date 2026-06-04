from config.navigation import PAGINAS
from views.dashboard import tela_dashboard
from database.db import inicializar_banco 
#, inserir_requisitos_teste
from views.login import tela_login
from views.login import tela_login
from views.dashboard import tela_dashboard



import streamlit as st

st.set_page_config(
    page_title="ReqFlow",
    layout="wide"
)

inicializar_banco()
#inserir_requisitos_teste()

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:

    tela_login()

else:

    pagina = tela_dashboard()

    PAGINAS[pagina]()


