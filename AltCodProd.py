import streamlit as st
import pandas as pd
import io
import requests
from openpyxl import load_workbook

def altcodprod():
    # Função para converter strings numéricas para inteiros, removendo quaisquer vírgulas
    def custom_converter(number_str):
        try:
            if isinstance(number_str, str):
                return int(number_str.replace(',', ''))
            else:
                return number_str
        except:
            return number_str

    # Função para ler o arquivo XLSX do link raw do GitHub
    def load_data(url):
        response = requests.get(url)
        content = response.content
        xls_file = io.BytesIO(content)
        df = pd.read_excel(xls_file, engine="openpyxl",
                           converters={'Código de Compra': custom_converter, 'Código de Venda': custom_converter})
        return df

    # Carrega os dados
    url = "https://raw.githubusercontent.com/mateus4422/cestcat/cestcat/Tabela%20de%20c%C3%B3digo.xlsx"
    data = load_data(url)

    st.title("Alteração de Código do Produto")

    # Filtros na mesma janela da tabela
    venda_filter = st.text_input("Filtrar por Código de Venda:")
    ean_filter = st.text_input("Filtrar por EAN de Compra:")
    
    # Remove vírgulas da coluna Código de Venda
    data["Código de Venda"] = data["Código de Venda"].astype(str).str.replace(',', '')

    # Remove vírgulas da coluna Código de Compra
    data["Código de Compra"] = data["Código de Compra"].astype(str).str.replace(',', '')

    # Filtros
    if venda_filter:
        data = data[data["Código de Venda"].astype(str).str.contains(venda_filter)]

    if ean_filter:
        data = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Exibe a tabela
    st.write(data)

if __name__ == "__main__":
    altcodprod()
