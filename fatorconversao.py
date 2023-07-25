import streamlit as st
import pandas as pd
import base64
import io

def fatorconv():
    # Carregue o arquivo Excel da URL
    url = 'https://github.com/mateus4422/cestcat/raw/cestcat/Fator%20de%20convers%C3%A3o.xlsx'
    df = pd.read_excel(url, engine='openpyxl')

    st.title("Fator de Conversão")

    # Filtro para pesquisar por Código do Produto
    cod_produto = st.text_input("Digite o código do produto (Código do Produto):")

    # Filtrar o dataframe com base no Código do Produto inserido
    filtered_df = df[df['Código Produto'].astype(str).str.contains(cod_produto)]

    # Selecionar apenas as colunas desejadas
    columns_to_display = ['Código do Produto', 'Descrição', 'unimed', 'Fator', 'NCM', 'Produto ST']
    filtered_df = filtered_df[columns_to_display]

    st.write(f"Resultados para Código do Produto: {cod_produto}")
    st.dataframe(filtered_df)

    # Crie um objeto BytesIO para salvar o dataframe
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Escreva o dataframe para o objeto BytesIO
    filtered_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Importante: feche o writer ou o arquivo não será salvo
    writer.close()

    # Retorne ao início do stream
    output.seek(0)

    # Crie um link para baixar o dataframe
    excel_file = output.getvalue()
    b64 = base64.b64encode(excel_file)
    dl_file = b64.decode()

    href = f'<a href="data:application/octet-stream;base64,{dl_file}" download="Fator_de_Conversao.xlsx">Baixar o Arquivo</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    fatorconv()
