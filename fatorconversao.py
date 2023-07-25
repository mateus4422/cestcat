import streamlit as st
import pandas as pd
import requests
from io import BytesIO

def fatorconv():
    # Link para o arquivo Excel hospedado no GitHub (Raw)
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Fator%20de%20convers%C3%A3o.xlsx"

    # Baixar o arquivo Excel usando requests
    response = requests.get(url)
    content = response.content

    # Carregar o arquivo Excel em um DataFrame
    df = pd.read_excel(BytesIO(content), engine='openpyxl')

    st.title("Fator de Conversão")

    # Input para o filtro no "Código do Produto"
    codigo_produto = st.text_input("Digite o Código do Produto para filtrar:")

    # Filtrar o DataFrame com base no Código do Produto
    if codigo_produto:
        df_filtered = df[df["Código do Produto"] == codigo_produto]
        if not df_filtered.empty:
            st.write("Resultados:")
            st.dataframe(df_filtered)
        else:
            st.warning("Nenhum resultado encontrado para o código do produto fornecido.")
    else:
        st.write("Digite um código de produto para começar.")

if __name__ == "__main__":
    fatorconv()
