import streamlit as st
import pandas as pd
import requests
import io 

def altcodprod():
    # Função para converter strings numéricas para inteiros, removendo quaisquer vírgulas
    def custom_converter(number_str):
        if isinstance(number_str, str) and ',' in number_str:
            return int(number_str.replace(',', ''))
        else:
            return number_str

    # Função para ler o arquivo XLSX do link raw do GitHub
    def load_data(url):
        response = requests.get(url)
        with open('conversao_codigo.xlsx', 'wb') as f:
            f.write(response.content)
        df = pd.read_excel('conversao_codigo.xlsx', engine="openpyxl",
                           converters={'Código de Compra': custom_converter, 'Código de Venda': custom_converter})
        return df

    # Carrega os dados
    url = "https://github.com/mateus4422/cestcat/raw/cestcat/Convers%C3%A3o%20de%20C%C3%B3digo.xlsx"
    data = load_data(url)

    st.title("Alteração de Código do Produto")


    # Filtros na mesma janela da tabela
    venda_filter = st.text_input("Filtrar por Código de Venda:")
    compra_filter = st.text_input("Filtrar por Código de Compra:")
    ean_filter = st.text_input("Filtrar por EAN:")
    
    # Remove vírgulas das colunas Código de Venda e Código de Compra
    data["Código de Venda"] = data["Código de Venda"].astype(str).str.replace(',', '')
    data["Código de Compra"] = data["Código de Compra"].astype(str).str.replace(',', '')

    # Filtros
    if venda_filter:
        data = data[data["Código de Venda"].astype(str).str.contains(venda_filter)]

    if compra_filter:
        data = data[data["Código de Compra"].astype(str).str.contains(compra_filter)]

    if ean_filter:
        data = data[data["EAN de Compra"].astype(str).str.contains(ean_filter)]

    # Exibe a tabela
    st.write(data)

    # Botão de download
    bytes_to_write = io.BytesIO()
    with pd.ExcelWriter(bytes_to_write, engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name='Sheet1')
    bytes_to_write.seek(0)  # retornar ao início do objeto BytesIO
    st.download_button('Baixar o arquivo', bytes_to_write, file_name='conversao_codigo.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    altcodprod()
