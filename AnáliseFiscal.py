import streamlit as st
from openpyxl import load_workbook
from io import BytesIO
import requests

def analisefiscal():
    # Título da aplicação
    st.title("Análise Fiscal")

    # Nome do arquivo da planilha
    file_name = "Cabeçalho_Análise.xlsx"

    # Montar a URL do arquivo no GitHub
    url = f"https://github.com/mateus4422/cestcat/raw/cestcat/{file_name}"

    try:
        # Fazer o download do arquivo usando a biblioteca requests
        response = requests.get(url)
        content = response.content

        # Carregar a planilha usando a biblioteca openpyxl
        wb = load_workbook(filename=BytesIO(content), read_only=True)
        ws = wb.active

        # Ler os dados da planilha e exibi-los no Streamlit
        data = [[cell.value for cell in row] for row in ws.iter_rows()]
        st.table(data)

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo xlsx: {e}")
