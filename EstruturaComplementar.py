import streamlit as st
import pandas as pd
import io
import requests
import base64

def estruturacomplementar():
    def carregar_github_raw(url):
        data = requests.get(url).content
        return pd.read_excel(io.BytesIO(data))

    def converter_para_inteiro(x):
        if pd.isna(x) or str(x).strip() == '':
            return None
        else:
            return int(float(str(x).replace(',', '')))

    def download_link(dataframe, filename, text):
        csv = dataframe.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" target="_blank">{text}</a>'
        return href

    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabeçalho%20Complementar%20-%20PROCFIT.xlsx"
    df_git = carregar_github_raw(url)

    st.write("## Tabela do GitHub")
    st.write(df_git)

    file = st.file_uploader("Carregar arquivo xlsx", type=["xlsx"])

    if file:
        df_local = pd.read_excel(file)

        campos_para_converter = [3, 8]
        for campo in campos_para_converter:
            df_local.iloc[:, campo] = df_local.iloc[:, campo].apply(converter_para_inteiro)

        tipos_dados = ['str', 'int', 'float', 'datetime64[ns]']
        cols = df_local.columns
        tipos_colunas = {}
        for col in cols:
            tipo = st.selectbox(f"Selecione o tipo de dado para a coluna {col}", tipos_dados)
            tipos_colunas[col] = tipo
        df_local = df_local.astype(tipos_colunas)

        df_final = df_git.append(df_local, ignore_index=True)

        st.write("##Tabela Estrutural da Complementar - PROCFIT")
        st.write(df_final)

        dataframes = [df_final[i:i+20000] for i in range(0, len(df_final), 20000)]

        for i, df_split in enumerate(dataframes):
            st.write(f"## Tabela {i+1}")
            st.write(df_split)

            if st.button(f"Gerar Download  {i+1}"):
                df_copy = df_split.copy()
                df_copy.columns = df_copy.columns.str.replace(',', '')

                link = download_link(df_copy, f"dataframe_{i+1}.csv", f"Clique aqui para baixar a tabela {i+1}")
                st.markdown(link, unsafe_allow_html=True)

estruturacomplementar()
