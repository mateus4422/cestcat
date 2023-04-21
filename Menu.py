import streamlit as st
from pdf2image import convert_from_path
from reg1100 import cat1100
from Manual import exibir_pdf
from cest import cest
from efd_0220 import fatorconversao
from c100_c170 import c100_c170

def main():

    menu_options = ["Selecione uma opção", "CAT", "EFD", "MANUAIS", "PRODUTOS"]
    choice = st.sidebar.selectbox("Menu", menu_options)

    if choice == "CAT":
        cat_options = ["Selecione uma opção", "Registro 1100", "Outros"]
        cat_choice = st.sidebar.selectbox("CAT", cat_options)

        if cat_choice == "Registro 1100":
            st.subheader("CAT - Registro 1100")
            cat1100()

        elif cat_choice == "Outros":
            # Adicione outras funcionalidades relacionadas ao CAT
            pass

    elif choice == "EFD":
        st.subheader("EFD")
        efd_options = ["Selecione uma opção", "Fator de Conversão", "C100-C170"]
        efd_choice = st.sidebar.selectbox("EFD", efd_options)

        if efd_choice == "Fator de Conversão":
            fatorconversao()

        elif efd_choice == "C100-C170":
            c100_c170()

    elif choice == "MANUAIS":
        st.subheader("Manuais")
        exibir_pdf()

    elif choice == "PRODUTOS":
        st.subheader("Produtos - CEST")
        cest()

if __name__ == "__main__":
    main()
