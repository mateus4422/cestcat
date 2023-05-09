import streamlit as st
from reg1100 import cat1100
from Manual import exibir_pdf
from cest import cest
from efd_0220 import fatorconversao
from c100_c170 import c100_c170
from Inventário import inventario
from ProdST import tb_produtos
from AltCodProd import altcodprod
from EstruturaComplementar import estruturacomplementar
from AnaliseFiscal import cabecalhoanalise

def main():

    menu_options = ["Selecione uma opção", "CAT", "EFD", "MANUAIS", "PRODUTOS", "ANÁLISE FISCAL", "COMPLEMENTAR"]
    choice = st.sidebar.selectbox("Menu", menu_options)

    if choice == "CAT":
        cat_options = ["Selecione uma opção", "Registro 1100"]
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
        st.subheader("Produtos")
        produtos_options = ["Selecione uma opção", "Cest", "Inventário", "Tabela de Produtos", "Tabela de Alteração de Código"]
        produtos_choice = st.sidebar.selectbox("PRODUTOS", produtos_options)

        if produtos_choice == "Cest":
            cest()
        elif produtos_choice == "Inventário":
             inventario()
        elif produtos_choice == "Tabela de Produtos":
            tb_produtos()
        elif produtos_choice == "Tabela de Alteração de Código":
            altcodprod()

    elif choice == "COMPLEMENTAR":
         st.subheader("Complementar")
         complementar_options = ["Selecione uma opção", "Estrutura Complementar - PROCFIT"]
         complementar_choice = st.sidebar.selectbox("COMPLEMENTAR", complementar_options)

         if complementar_choice == "Estrutura Complementar - PROCFIT":
             estruturacomplementar()
            
    elif choice == "ANÁLISE FISCAL":
         st.subheader("Análise Fiscal")
         analisefiscal_options = ["Selecione uma opção", "Análise Fiscal"]
         analisefiscal_choice = st.sidebar.selectbox("ANÁLISE FISCAL", analisefiscal_options)

         if analisefiscal_choice == "Análise Fiscal":
             estruturacomplementar()

if __name__ == "__main__":
    main()
