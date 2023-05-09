import streamlit as st
import pandas as pd
import io
import requests
from openpyxl import load_workbook

def altcodprod():
    # Função para ler o arquivo XLSX do link raw do GitHub
    def custom_converter(number_str):
        return int(number_str.replace(',', ''))

    # Função para ler o arquivo XLSX do link raw do GitHub
    def load_data(url):
        response = requests.get(url)
        content = response.content
        xls_file = io.BytesIO(content)
        df = pd.read_excel(xls_file, engine="openpyxl",
                           converters={'Código de Compra': custom_converter, 'Código de Venda': custom_converter})
        return df

    # Carrega os dados
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Tabela%20de%20código.xlsx"
    data = load_data(url)

    st.title("Alteração de Código do Produto")

    # Filtros na mesma janela da tabela
    ncm_filter = st.text_input("Filtrar por NCM:")
    ean_filter = st.text_input("Filtrar por EAN:")
    cod_venda_type = st.selectbox("Tipo de dado para Código de Venda:", ("", "Inteiro", "Decimal", "Data"))
    cod_compra_type = st.selectbox("Tipo de dado para Código de Compra:", ("", "Inteiro", "Decimal", "Data"))

    # Converte Código de Venda para o tipo de dado selecionado
    if cod_venda_type == "Inteiro":
        data["Código de Venda"] = data["Código de Venda"].astype(int, errors='ignore')
    elif cod_venda_type == "Decimal":
        data["Código de Venda"] = data["Código de Venda"].astype(float, errors='ignore')
    elif cod_venda_type == "Data":
        data["Código de Venda"] = pd.to_datetime(data["Código de Venda"], errors='coerce')

    # Converte Código de Compra para o tipo de dado selecionado
    if cod_compra_type == "Inteiro":
        data["Código de Compra"] = data["Código de Compra"].astype(int, errors='ignore')
    elif cod_compra_type == "Decimal":
        data["Código de Compra"] = data["Código de Compra"].astype(float, errors='ignore')
    elif cod_compra_type == "Data":
        data["Código de Compra"] = pd.to_datetime(data["Código de Compra"], errors='coerce')

    # Aplica o filtro de NCM
    if ncm_filter:
        data = data[data["NCM"].astype(str).str.contains(ncm_filter)]

    # Aplica o filtro de EAN
    if ean_filter:
        data = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Exibe a tabela
    st.write(data)
