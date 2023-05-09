import pandas as pd
import streamlit as st
import glob

def process_efd_file(file):
    lines = file.readlines()

    reg2 = []
    reg3 = []

    for line in lines:
        decoded_line = line.decode('utf-8')
        if decoded_line.startswith("|C100|"):
            reg2.append(decoded_line.strip().split("|"))
        elif decoded_line.startswith("|C170|"):
            reg3.append(decoded_line.strip().split("|"))

    df_c100 = pd.DataFrame(reg2[1:], columns=reg2[0])
    df_c170 = pd.DataFrame(reg3[1:], columns=reg3[0])

    df_merged = pd.concat([df_c100.assign(dummy_key=1), df_c170.assign(dummy_key=1)], ignore_index=True).merge(
        df_c100, on="dummy_key", how="outer", suffixes=("_c100", "_c170")
    ).drop("dummy_key", axis=1)

    return df_merged

def cabecalhoanalise():
    # URL do link raw do arquivo Excel no GitHub
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabe%C3%A7alho_An%C3%A1lise.xlsx"

    # Carregue a planilha em um DataFrame do Pandas
    df = pd.read_excel(url, engine='openpyxl')

    # Exiba apenas o cabeçalho da planilha no Streamlit
    st.write("Cabeçalho da planilha de análise fiscal:")
    st.write(df.head(0))

cabecalhoanalise()

uploaded_files = st.file_uploader("Escolha os arquivos EFD em TXT", type="txt", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        processed_efd = process_efd_file(file)
        st.write(processed_efd)
