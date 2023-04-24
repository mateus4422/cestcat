import pandas as pd
import streamlit as st

def inventario():
    def load_efd_file(file):
        content = file.read().decode("latin-1")
        lines = content.splitlines()
        records = [line.strip().split("|") for line in lines]

        h010_records = []
        for record in records:
            if len(record) > 1 and record[1] == "H010":
                h010_records.append(record)

        df_efd = pd.DataFrame(h010_records).iloc[:, [1, 2, 3, 4]]
        df_efd.columns = ["REG", "COD_PRODUTO_EFD", "UNID", "QTD_EFD"]
        df_efd["QTD_EFD"] = df_efd["QTD_EFD"].apply(lambda x: int(float(x.replace(",", "."))))
        return df_efd


    def load_cat_file(file):
        content = file.read().decode("latin-1")
        lines = content.splitlines()
        records = [line.strip().split("|") for line in lines]

        cat_records = []
        for record in records:
            if len(record) > 1 and record[0] == "1050":
                cat_records.append(record)

        df_cat = pd.DataFrame(cat_records).iloc[:, [1, 4]]
        df_cat.columns = ["COD_PRODUTO_CAT", "QTD_CAT"]
        df_cat["QTD_CAT"] = df_cat["QTD_CAT"].apply(lambda x: int(float(x.replace(",", "."))))
        return df_cat


    def compare_dataframes(df_efd, df_cat):
     merged_df = pd.merge(df_efd, df_cat, left_on="COD_PRODUTO_EFD", right_on="COD_PRODUTO_CAT", how="inner")
     merged_df = merged_df[["COD_PRODUTO_EFD", "QTD_EFD", "QTD_CAT"]]
     merged_df['COMPARACAO'] = merged_df.apply(lambda row: 'Igual' if row['QTD_EFD'] == row['QTD_CAT'] else 'Diferente', axis=1)
     merged_df['DIFERENCA'] = merged_df['QTD_EFD'] - merged_df['QTD_CAT']  # Adicione esta linha para calcular a diferença
     return merged_df


    st.title("Comparação de Quantidades - EFD e CAT")

    uploaded_efd_file = st.file_uploader("Carregue o arquivo EFD (.txt)", type="txt")
    uploaded_cat_file = st.file_uploader("Carregue o arquivo CAT (.txt)", type="txt")

    if uploaded_efd_file:
        df_efd = load_efd_file(uploaded_efd_file)
        if "H010" in df_efd["REG"].values:
            st.write("Arquivo contém H010")
        else:
            st.write("Registro H010 não encontrado no arquivo")

    if uploaded_cat_file:
        df_cat = load_cat_file(uploaded_cat_file)



    if uploaded_efd_file and uploaded_cat_file:
        comparison_df = compare_dataframes(df_efd, df_cat)
        st.write("COMPARATIVO DE QUANTIDADE DA EFD E CAT:")
        st.write(comparison_df)
