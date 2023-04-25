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
    df = pd.read_excel(xls_file, engine="openpyxl")
    return df

# Carrega os dados
url = "INSIRA_AQUI_O_SEU_LINK_RAW_DO_GITHUB"
data = load_data(url)

# Converte os códigos de compra e venda para inteiros
data['Código de Compra'] = data['Código de Compra'].astype(int)
data['Código de Venda'] = data['Código de Venda'].astype(int)

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
