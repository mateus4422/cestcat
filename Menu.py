import streamlit as st
from reg1100 import cat1100
from Manual import exibir_pdf
from cest import cest
from efd_0220 import fatorconversao
from c100_c170 import c100_c170
from Inventário import inventario
from ProdST import tb_produtos
from AltCodProd import altcodprod
from aliquota import tb_aliquota

def main():

    menu_options = ["Selecione uma opção", "CAT", "EFD", "MANUAIS", "PRODUTOS", "COMPLEMENTAR","ALÍQUOTA"]
    choice = st.sidebar.radio("Menu", menu_options)

    if choice == "CAT":
        st.subheader("CAT")
        cat1100()

    elif choice == "EFD":
        st.subheader("EFD")
        efd_options = ["Fator de Conversão", "C100-C170"]
        efd_choice = st.sidebar.radio("EFD", efd_options)

        if efd_choice == "Fator de Conversão":
            fatorconversao()

        elif efd_choice == "C100-C170":
            c100_c170()

    elif choice == "MANUAIS":
        st.subheader("Manuais")
        exibir_pdf()

    elif choice == "PRODUTOS":
        st.subheader("Produtos")
        produtos_options = ["Cest", "Inventário", "Tabela de Produtos", "Tabela de Alteração de Código"]
        produtos_choice = st.sidebar.radio("PRODUTOS", produtos_options)

        if produtos_choice == "Cest":
            cest()
        elif produtos_choice == "Inventário":
            inventario()
        elif produtos_choice == "Tabela de Produtos":
            tb_produtos()
        elif produtos_choice == "Tabela de Alteração de Código":
            altcodprod()
            
    elif choice == "ALÍQUOTA":
        st.subheader("Alíquota")
        aliquota_options = ["Alíquota"]
        aliquota_choice = st.sidebar.radio("ALÍQUOTA", aliquota_options)

        if aliquota_choice == "Alíquota":
            tb_aliquota()


if __name__ == "__main__":
    main()
