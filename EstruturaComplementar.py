import streamlit as st
import pandas as pd
import io
import requests
import clipboard

def estruturacomplementar ():
    def carregar_github_raw(url):
        data = requests.get(url).content
        return pd.read_excel(io.BytesIO(data))

    # Função para converter valores para inteiros, tratando NaN e valores vazios
    def converter_para_inteiro(x):
        if pd.isna(x) or str(x).strip() == '':
            return None
        else:
            return int(float(str(x).replace(',', '')))

    # URL do arquivo raw do GitHub
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabeçalho%20Complementar%20-%20PROCFIT.xlsx"
    df_git = carregar_github_raw(url)

    st.write("## Tabela do GitHub")
    st.write(df_git)

    file = st.file_uploader("Carregar arquivo xlsx", type=["xlsx"])

    if file:
        df_local = pd.read_excel(file)

        # Removendo vírgulas e convertendo para números inteiros nos campos 4 e 8
        campos_para_converter = [3, 8]  # Os índices são baseados em 0, então 3 representa o campo 4 e 8 representa o campo "Registro Anvisa Origem NFE"
        for campo in campos_para_converter:
            df_local.iloc[:, campo] = df_local.iloc[:, campo].apply(converter_para_inteiro)

        # Incluindo seleção de tipo de dados para cada coluna
        tipos_dados = ['str', 'int', 'float', 'datetime64[ns]']
        cols = df_local.columns
        tipos_colunas = {}
        for col in cols:
            tipo = st.selectbox(f"Selecione o tipo de dado para a coluna {col}", tipos_dados)
            tipos_colunas[col] = tipo
        df_local = df_local.astype(tipos_colunas)

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
                # Cria um novo DataFrame com cabeçalhos sem vírgulas
                df_copy = df_split.copy()
                df_copy.columns = df_copy.columns.str.replace(',', '')

                # Copia o DataFrame para a área de transferência
                clipboard.copy(df_copy.to_csv(index=False))
                st.success(f"DataFrame {i+1} copiado para a área de transferência")

estruturacomplementar()
