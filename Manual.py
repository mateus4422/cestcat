import os
import streamlit as st
from pdf2image import convert_from_path

def exibir_pdf():
    diretorio = r"C:\Users\Mateus Ramos\PycharmProjects\Python\Sistema\Manuais"
    pdfs = [os.path.join(diretorio, f) for f in os.listdir(diretorio) if f.endswith('.pdf')]

    if not pdfs:
        st.warning("Nenhum arquivo PDF encontrado na pasta.")
    else:
        st.sidebar.title("Selecione um arquivo PDF")
        for arquivo in pdfs:
            if st.sidebar.button(os.path.basename(arquivo)):
                st.title(f"Leitor de PDF: {os.path.basename(arquivo)}")
                imagens = convert_from_path(arquivo)
                for pagina, imagem in enumerate(imagens):
                    st.image(imagem, caption=f"Página {pagina+1}", use_column_width=True)
