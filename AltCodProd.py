import streamlit as st
import pandas as pd
import io
import requests
from openpyxl import load_workbook

def altcodprod()
    # Função para ler o arquivo XLSX do link raw do GitHub
    def load_data(url):
        response = requests.get(url)
        content = response.content
        xls_file = io.BytesIO(content)
        df = pd.read_excel(xls_file, engine="openpyxl")
        return df

    # Carrega os dados
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Tabela%20de%20código.xlsx"
    data = load_data(url)

    st.title("Visualização de arquivo XLSX")

    # Filtro de NCM
    ncm_filter = st.sidebar.text_input("Filtrar por NCM:")
    filtered_data_ncm = data[data["NCM"].astype(str).str.contains(ncm_filter)]

    # Filtro de EAN
    ean_filter = st.sidebar.text_input("Filtrar por EAN:")
    filtered_data_ean = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Aplica os filtros
    filtered_data = filtered_data_ncm.merge(filtered_data_ean)

    # Exibe a tabela
    st.write(filtered_data)
