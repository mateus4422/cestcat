import streamlit as st
from visualizacao import visualizacao_cf
from download import download_cf

PAGES = {
    "Visualização de CF": visualizacao_cf,
    "Download de CF": download_cf
}

def main():
    st.sidebar.title("Menu de Navegação")
    choice = st.sidebar.radio("Escolha uma opção", list(PAGES.keys()))
    page = PAGES[choice]
    page()

if __name__ == "__main__":
    main()
