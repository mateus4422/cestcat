import streamlit as st
import pandas as pd
import io
import requests
import clipboard

def estruturacomplementar():# Função para carregar o arquivo do GitHub
    def carregar_github_raw(url):
        data = requests.get(url).content
        return pd.read_excel(io.BytesIO(data))

    # URL do arquivo raw do GitHub
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabeçalho%20Complementar%20-%20PROCFIT.xlsx"
    df_git = carregar_github_raw(url)

    st.write("## Tabela do GitHub")
    st.write(df_git)

    file = st.file_uploader("Carregar arquivo xlsx", type=["xlsx"])

    if file:
    df_local = pd.read_excel(file).convert_dtypes()
    
         # Lista de índices das colunas que devem ser convertidas
        cols_to_convert = [4, 9]
        for col_idx in cols_to_convert:
            df_local.iloc[:, col_idx] = df_local.iloc[:, col_idx].astype(str).str.replace(',', '').astype(int)

        # Preenchendo a tabela
        df_final = df_git.append(df_local, ignore_index=True)

        st.write("## Tabela carregada e preenchida")
        st.write(df_final)

        # Dividindo em DataFrames de no máximo 20 mil linhas
        dataframes = [df_final[i:i+20000] for i in range(0, len(df_final), 20000)]

        for i, df_split in enumerate(dataframes):
            st.write(f"## DataFrame {i+1}")
            st.write(df_split)

            if st.button(f"Copiar DataFrame {i+1}"):
                clipboard.copy(df_split.to_csv(index=False))
                st.success(f"DataFrame {i+1} copiado para a área de transferência")
