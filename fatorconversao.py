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

if __name__ == "__main__":
    fatorconv()
