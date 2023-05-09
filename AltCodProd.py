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
    cod_venda_format = st.text_input("Formato do Código de Venda (Ex: ###-#####):")
    cod_compra_format = st.text_input("Formato do Código de Compra (Ex: #####):")

    # Remove vírgulas da coluna Código de Venda
    data["Código de Venda"] = data["Código de Venda"].str.replace(',', '')

    # Remove vírgulas da coluna Código de Compra
    data["Código de Compra"] = data["Código de Compra"].str.replace(',', '')

    # Formatação do Código de Venda
    if cod_venda_format:
        data["Código de Venda"] = data["Código de Venda"].apply(lambda x: format(int(x), cod_venda_format) if pd.notnull(x) else "")
    # Formatação do Código de Compra
    if cod_compra_format:
        data["Código de Compra"] = data["Código de Compra"].apply(lambda x: format(int(x), cod_compra_format) if pd.notnull(x) else "")

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

    # Filtros
    if ncm_filter:
        data = data[data["NCM"].astype(str).str.contains(ncm_filter)]

    if ean_filter:
        data = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Exibe a tabela
    st.write(data)


if __name__ == "__main__":
    altcodprod()

