import streamlit as st
import pandas as pd
import base64
import io

def fatorconv():
    # URL do arquivo Excel
    url = 'https://github.com/mateus4422/cestcat/raw/cestcat/Fator%20de%20convers%C3%A3o.xlsx'

    # Tente baixar o arquivo e ler com o pandas
    try:
        df = pd.read_excel(url, engine='openpyxl')
    except Exception as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
        return

    st.title("Fator de Conversão")

    # Filtro para pesquisar por Código do Produto
    cod_produto = st.text_input("Digite o código do produto (Código do Produto):")

    # Filtrar o dataframe com base no Código do Produto inserido
    filtered_df = df[df['Código do Produto'].astype(str).str.contains(cod_produto)]

    # Selecionar apenas as colunas desejadas
    columns_to_display = ['Código do Produto', 'Descrição', 'unimed', 'Fator', 'NCM', 'Produto ST']
    filtered_df = filtered_df[columns_to_display]

    st.write(f"Resultados para Código do Produto: {cod_produto}")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    fatorconv()
