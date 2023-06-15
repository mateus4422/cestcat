import streamlit as st
import pandas as pd
import requests
import io

def tb_aliquota():
    # URL do arquivo Excel
    url = 'https://github.com/mateus4422/cestcat/raw/cestcat/Aliquota.xlsx'

    # Faça uma solicitação GET para a URL
    r = requests.get(url)

    # Certifique-se de que a solicitação foi bem-sucedida
    if r.status_code == 200:
        # Leia os dados do Excel em um DataFrame do Pandas
        df = pd.read_excel(io.BytesIO(r.content), engine='openpyxl')

        # Remova as vírgulas da coluna 'Código de Venda'
        df['Código de Venda'] = df['Código de Venda'].str.replace(',', '')

        st.title("Tabela de Alíquota")

        # Filtros para pesquisar por 'Código de Venda'
        cod_venda = st.text_input("Digite o 'Código de Venda':")

        # Filtrar o dataframe com base nos valores inseridos
        filtered_df = df[df['Código de Venda'].astype(str).str.contains(cod_venda)]

        st.write(f"Resultados para 'Código de Venda': {cod_venda}")
        st.dataframe(filtered_df)

        # Crie um link para baixar o DataFrame como um arquivo CSV
        csv = filtered_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="aliquota.csv">Clique aqui para baixar o arquivo CSV filtrado</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.write(f"Não foi possível obter os dados do arquivo Excel. Código de status HTTP: {r.status_code}")


# Chamar a função tb_aliquota()
tb_aliquota()
