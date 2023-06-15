import streamlit as st
import pandas as pd

def cat1100():
    def processa_arquivo(arquivo, chave_produto=None):
        linhas = arquivo.readlines()
        resultados = []

        for linha in linhas:
            if linha.startswith(b"1100"):
                campos = linha.decode('utf-8').split('|')
                if chave_produto is None or campos[1] == chave_produto:
                    item_produto = campos[3]
                    codigo_produto = campos[5]
                    cfop = campos[6]
                    valor = campos[8].replace(',', '.')
                    if valor:
                        ressarcimento = float(valor)
                    else:
                        ressarcimento = 0
                    resultados.append(
                        {"Arquivo": arquivo.name, "Chave do Produto": campos[1], "Item do Produto": item_produto,
                         "Código do Produto": codigo_produto, "CFOP": cfop, "Ressarcimento": ressarcimento})

        return resultados


    st.write(
        "Carregue um ou mais arquivos CAT (formato TXT) e insira a chave do produto (opcional) para visualização dos valores da cat")

    uploaded_files = st.file_uploader("Escolha os arquivos", type=["txt"], accept_multiple_files=True)
    chave_produto = st.text_input("Digite a chave do produto (opcional)")
    resultados = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if chave_produto:
                resultados.extend(processa_arquivo(uploaded_file, chave_produto))
            else:
                resultados.extend(processa_arquivo(uploaded_file))

        df = pd.DataFrame(resultados)
        total_ressarcimento = df["Ressarcimento"].sum()
        st.write(df)
        st.write(
            f"O valor total de ressarcimento para todos os arquivos e a chave do produto fornecida (se houver) é: R$ {total_ressarcimento:.2f}")
