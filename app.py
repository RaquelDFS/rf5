import streamlit as st
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from config.navigation import PAGINAS
from database.db import inicializar_banco
from utils.style import carregar_css
from views.dashboard import tela_dashboard
from views.login import tela_login


CHAVE_LOGIN = "reqflow_login_local"
TEMPO_LOGIN_SEGUNDOS = 60 * 60 * 8


def obter_assinador_login():
    return URLSafeTimedSerializer(CHAVE_LOGIN)


def restaurar_login_por_token():
    if st.session_state.get("logado"):
        return

    token = st.query_params.get("auth")

    if not token:
        return

    assinador = obter_assinador_login()

    try:
        dados = assinador.loads(
            token,
            max_age=TEMPO_LOGIN_SEGUNDOS
        )
    except SignatureExpired:
        st.query_params.clear()
        return
    except BadSignature:
        st.query_params.clear()
        return

    if not dados:
        return

    st.session_state["id_usuario"] = dados.get("id_usuario")
    st.session_state["usuario"] = dados.get("usuario")
    st.session_state["funcao"] = dados.get("funcao")
    st.session_state["logado"] = True

    if "pagina_atual" not in st.session_state:
        st.session_state["pagina_atual"] = "Início"


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

restaurar_login_por_token()

if not st.session_state["logado"]:
    tela_login()
else:
    pagina = tela_dashboard()

    if pagina in PAGINAS:
        PAGINAS[pagina]()
    else:
        st.error("Página não encontrada.")