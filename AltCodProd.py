import pandas as pd
import io
import requests
import streamlit as st

def load_data(url):
    response = requests.get(url)
    content = response.content
    xls_file = io.BytesIO(content)
    df = pd.read_excel(xls_file, engine="openpyxl")
    return df

def altcodprod():
    # Carrega os dados
    url = "https://raw.githubusercontent.com/mateus4422/cestcat/cestcat/Tabela%20de%20c%C3%B3digo.xlsx"
    data = load_data(url)

    st.title("Visualização de Dados do Excel")
    st.write(data)

if __name__ == "__main__":
    altcodprod()
