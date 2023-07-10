import streamlit as st
import pandas as pd
import io
import chardet
import base64
import random

def fatorconversao():
    def download_link_csv(df, filename, link_text):
        csv = df.to_csv(index=False, encoding='utf-8')
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" target="_blank">{link_text}</a>'
        return href

    def read_efd_file(uploaded_file):
        # Detectar a codificação do arquivo
        file_content = uploaded_file.read()
        result = chardet.detect(file_content)
        char_encoding = result['encoding']

        # Usar latin-1 como codificação padrão caso a detecção falhe
        if char_encoding is None:
            char_encoding = 'latin-1'

        # Converter para latin-1 se necessário
        if char_encoding != 'latin-1':
            file_content = file_content.decode(char_encoding, errors='ignore').encode('utf-8')

        file_like = io.BytesIO(file_content)
        lines = file_like.readlines()
        data = []
        current_0200 = None
        has_0220 = False

        for line in lines:
            line = line.decode('latin-1').strip()

            if line.startswith('|0200|'):
                current_0200 = line.split('|')
                has_0220 = False

            elif line.startswith('|0220|'):
                has_0220 = True
                current_0220 = line.split('|')
                if current_0200 is not None:
                    data.append(current_0200 + current_0220)

        df = pd.DataFrame(data)

        # Excluir as colunas especificadas
        columns_to_drop = [0, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 4, 19, 6]
        df = df.drop(columns=columns_to_drop)

        # Renomear as colunas
        column_names = {1: 'REG', 2: 'COD_PRODUTO', 3: 'DESCRIÇÃO', 6: 'NCM', 8: 'CEST', 16: 'REG2', 17: 'UNIDADE', 18: 'FATOR'}
        df = df.rename(columns=column_names)

        return df

    st.title('Fator de Conversão')

    uploaded_files = st.file_uploader('Escolha um ou mais arquivos EFD em txt', type=['txt'],
                                      accept_multiple_files=True)

    if uploaded_files:
        df_combined_list = []  # Lista para armazenar os dataframes de cada arquivo

        for uploaded_file in uploaded_files:
            df_combined_list.append(read_efd_file(uploaded_file))  # Adicionar cada dataframe à lista

        if df_combined_list:
            df_combined = pd.concat(df_combined_list, ignore_index=True)  # Concatenar os dataframes em um único dataframe

            if not df_combined.empty:
                product_filter = st.text_input("Digite o código do produto para filtrar:")
                if product_filter:
                    filtered_df = df_combined[df_combined['COD_PRODUTO'].str.contains(product_filter)]
                    st.dataframe(filtered_df)
                    if not filtered_df.empty:
                        st.markdown(download_link_csv(filtered_df, 'tabela_filtrada.csv',
                                                      'Clique aqui para baixar a tabela filtrada em CSV'),
                                    unsafe_allow_html=True)
                else:
                    st.dataframe(df_combined)
                    st.markdown(download_link_csv(df_combined, 'tabela_exportada.csv',
                                                  'Clique aqui para baixar a tabela em CSV'),
                                unsafe_allow_html=True)
            else:
                st.write('Não foram encontrados registros |0200| e |0220| nos arquivos selecionados.')

fatorconversao()
