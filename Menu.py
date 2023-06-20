import streamlit as st
from reg1100 import cat1100
from cest import cest
from efd_0220 import fatorconversao
from c100_c170 import c100_c170
from Inventário import inventario
from ProdST import tb_produtos
from AltCodProd import altcodprod
from aliquota import tb_aliquota
from cat import cat_detalhes

def main():
  

    menu_options = ["CAT", "EFD", "PRODUTOS", "ALÍQUOTA", "CUPOM FISCAL"]
    choice = st.sidebar.radio("Menu", menu_options)

    if choice == "CAT":
        st.subheader("CAT")
        cat1_options = ["Detalhes - CAT", "Cálculo de Ressarcimento - CAT"]
        cat1_choice = st.sidebar.radio("CAT", cat1_options)

        if cat1_choice == "Detalhes - CAT":
            cat_detalhes()
        elif cat1_choice == "Cálculo de Ressarcimento - CAT":
            cat1100()

    elif choice == "EFD":
        st.subheader("EFD")
        efd_options = ["Fator de Conversão", "C100-C170"]
        efd_choice = st.sidebar.radio("EFD", efd_options)

        if efd_choice == "Fator de Conversão":
            fatorconversao()
        elif efd_choice == "C100-C170":
            c100_c170()

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
