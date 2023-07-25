import streamlit as st
import pandas as pd
import base64
import xlsxwriter
import io

def tb_produtos():
    # Carregue o arquivo Excel da URL
    url = 'https://github.com/mateus4422/cestcat/raw/cestcat/Planilha%20de%20Produtos.xlsx'
    df = pd.read_excel(url, engine='openpyxl')

    st.title("Tabela de Produtos")

    # Filtros para pesquisar por COD_PRODUTO e NCM
    cod_produto = st.text_input("Digite o código do produto (COD_PRODUTO):")
    ncm = st.text_input("Digite o NCM:")

    # Filtrar o dataframe com base nos valores inseridos
    filtered_df = df[df['COD_PRODUTO'].astype(str).str.contains(cod_produto) & df['NCM'].astype(str).str.contains(ncm)]

    # Obtenha os valores únicos na coluna PROD_ST
    unique_prod_st = df['PROD_ST'].unique()
    unique_prod_st.sort()

    # Crie um filtro de seleção usando o widget selectbox do Streamlit
    selected_prod_st = st.selectbox("Produto ST?:", unique_prod_st)

    # Filtrar o dataframe usando o valor selecionado
    filtered_df = filtered_df[filtered_df['PROD_ST'] == selected_prod_st]

    # Selecionar apenas as colunas desejadas
    columns_to_display = ['Código do Produto', 'ANVISA', 'Descrição', 'NCM', 'CEST', 'Aliquota', 'MVA', 'Cesta Básica']
    filtered_df = filtered_df[columns_to_display]

    st.write(f"Resultados para COD_PRODUTO: {cod_produto}, NCM: {ncm}, e PROD_ST: {selected_prod_st}")
    st.dataframe(filtered_df)

    # Crie um objeto BytesIO para salvar o dataframe
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Escreva o dataframe para o objeto BytesIO
    filtered_df.to_excel(writer, sheet_name='Sheet1')

    # Importante: feche o writer ou o arquivo não será salvo
    writer.close()

    # Retorne ao início do stream
    output.seek(0)

    # Crie um link para baixar o dataframe
    excel_file = output.getvalue()
    b64 = base64.b64encode(excel_file)
    dl_file = b64.decode()

    href = f'<a href="data:application/octet-stream;base64,{dl_file}" download="output.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    tb_produtos()
