import streamlit as st
from openpyxl import load_workbook

# Título da aplicação
st.title("Análise Fiscal")

# Solicitar o link raw do arquivo do GitHub
url = st.text_input("https://github.com/mateus4422/cestcat/raw/cestcat/Cabeçalho_Análise.xlsx")


# Carregar e exibir a planilha xlsx
if url:
    try:
        response = requests.get(url)
        wb = load_workbook(filename=BytesIO(response.content))
        ws = wb.active
        rows = list(ws.rows)
        data = []
        for row in rows:
            data.append([cell.value for cell in row])
        st.table(data)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo xlsx: {e}")
