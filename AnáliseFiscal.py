import pandas as pd
import streamlit as st


def cabecalhoanalise():
    # URL do link raw do arquivo Excel no GitHub
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabe%C3%A7alho_An%C3%A1lise.xlsx"

    # Carregue a planilha em um DataFrame do Pandas
    df = pd.read_excel(url, engine='openpyxl')

    # Exiba apenas o cabeçalho da planilha no Streamlit
    st.write("Cabeçalho da planilha de análise fiscal:")
    st.write(df.head(0))

    # Execute o script com o comando `streamlit run nome_do_arquivo.py`
