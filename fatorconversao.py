import streamlit as st
import pandas as pd

def fatorconv():
    # Carregue o arquivo Excel da URL
    url = 'https://github.com/mateus4422/cestcat/raw/cestcat/Fator%20de%20convers%C3%A3o.xlsx'
    df = pd.read_excel(url, engine='openpyxl')

    st.title("Fator de Conversão")

    st.dataframe(df)

if __name__ == "__main__":
    fatorconv()
