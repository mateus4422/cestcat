import streamlit as st
import pandas as pd
import io
import requests
from openpyxl import load_workbook

def altcodprod():
    # Função para ler o arquivo XLSX do link raw do GitHub
    def load_data(url):
        response = requests.get(url)
        content = response.content
        xls_file = io.BytesIO(content)
        df = pd.read_excel(xls_file, engine="openpyxl", converters={'Código de Compra': int, 'Código de Venda': int})
        return df

    # Carrega os dados
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Tabela%20de%20código.xlsx"
    data = load_data(url)

    st.title("Visualização de arquivo XLSX")

    # Filtros na mesma janela da tabela
    ncm_filter = st.text_input("Filtrar por NCM:")
    ean_filter = st.text_input("Filtrar por EAN:")

    # Aplica o filtro de NCM
    if ncm_filter:
        data = data[data["NCM"].astype(str).str.contains(ncm_filter)]

    # Aplica o filtro de EAN
    if ean_filter:
        data = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Exibe a tabela
    st.write(data)
