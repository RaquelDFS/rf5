import streamlit as st
from pathlib import Path


def carregar_css():
    caminho_css = Path("assets/style.css")

    if caminho_css.exists():
        with open(caminho_css, "r", encoding="utf-8") as arquivo:
            st.markdown(f"<style>{arquivo.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Arquivo de estilo não encontrado: assets/style.css")