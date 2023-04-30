import pandas as pd
import numpy as np
import streamlit as st

def e struturacomplementar():
    def converter_para_inteiro(x):
        if pd.isna(x):
            return None
        else:
            return int(str(x).replace('.', '').replace(',', ''))

    def estruturacomplementar():
        # Lendo arquivo do GitHub
        url = "https://github.com/mateus4422/cestcat/raw/cestcat/Cabeçalho%20Complementar%20-%20PROCFIT.xlsx"
        df_git = pd.read_excel(url)

        # Carregando arquivo do usuário
        arquivo_local = st.file_uploader("Selecione o arquivo a ser carregado:", type=["xlsx"])

        if arquivo_local is not None:
            df_local = pd.read_excel(arquivo_local)

            # Concatenando DataFrames
            df_concatenado = pd.concat([df_git, df_local], ignore_index=True)

            # Verificando se o DataFrame precisa ser dividido em partes menores
            if len(df_concatenado) > 20000:
                df_split = np.array_split(df_concatenado, len(df_concatenado) // 20000 + 1)
                for i, df in enumerate(df_split):
                    st.write(f"Parte {i+1}")
                    st.write(df)

            else:
                # Mostrando DataFrame
                st.write(df_concatenado)

                # Criando lista de opções de formatos
                opcoes_formatos = ['', 'Texto', 'Moeda', 'Inteiro', 'Decimal', 'Data']

                # Criando dicionário para mapear cada coluna ao seu formato
                formatos = {}
                for coluna in df_concatenado.columns:
                    formatos[coluna] = st.selectbox(f"Escolha o formato para a coluna {coluna}", opcoes_formatos)

                # Aplicando os formatos selecionados para cada coluna
                for coluna, formato in formatos.items():
                    if formato == 'Texto':
                        df_concatenado[coluna] = df_concatenado[coluna].astype(str)
                    elif formato == 'Moeda':
                        df_concatenado[coluna] = pd.to_numeric(df_concatenado[coluna].str.replace(',', '.'), errors='coerce')
                        df_concatenado[coluna] = df_concatenado[coluna].apply(lambda x: f"R$ {x:,.2f}" if not pd.isna(x) else None)
                    elif formato == 'Inteiro':
                        df_concatenado[coluna] = df_concatenado[coluna].apply(converter_para_inteiro)
                    elif formato == 'Decimal':
                        df_concatenado[coluna] = pd.to_numeric(df_concatenado[coluna].str.replace(',', '.'), errors='coerce')
                    elif formato == 'Data':
                        df_concatenado[coluna] = pd.to_datetime(df_concatenado[coluna], errors='coerce')

                # Mostrando DataFrame com os formatos selecionados
                st.write(df_concatenado)

    if __name__ == "__main__":
        estruturacomplementar()
