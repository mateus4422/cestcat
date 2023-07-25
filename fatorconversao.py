import streamlit as st
import pandas as pd

def fatorconv():
    # Link para o arquivo Excel hospedado no GitHub (Raw)
    url = "https://raw.githubusercontent.com/mateus4422/cestcat/cestcat/Fator%20de%20convers%C3%A3o.xlsx"

    # Carregar o arquivo Excel em um DataFrame
    df = pd.read_excel(url, engine='openpyxl')

    st.title("Fator de Conversão")

    # Exibir o DataFrame completo
    st.write("DataFrame Completo:")
    st.dataframe(df)

    # Input para o filtro no "Código do Produto"
    codigo_produto = st.text_input("Digite o Código do Produto para ver detalhes específicos:")

    # Filtrar o DataFrame com base no Código do Produto
    if codigo_produto:
        df_filtered = df[df["Código do Produto"].astype(str).str.contains(codigo_produto)]
        if not df_filtered.empty:
            st.write(f"Detalhes para o Código do Produto: {codigo_produto}")
            st.dataframe(df_filtered)
        else:
            st.warning("Nenhum resultado encontrado para o código do produto fornecido.")

if __name__ == "__main__":
    fatorconv()
