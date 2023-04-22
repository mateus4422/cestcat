import streamlit as st
import pandas as pd
import io
import base64

def c100_c170():
    def extract_records(file, encoding):
        combined_records = []
        current_c100 = None

        for line in file:
            if line.startswith("|C100|"):
                current_c100 = ['C100'] + line.strip().split("|")[2:]
            elif line.startswith("|C170|") and current_c100 is not None:
                c170 = ['C170'] + line.strip().split("|")[2:]
                combined_records.append(current_c100 + c170)

        df = pd.DataFrame(combined_records)
        df = df.drop(columns=list(range(16,30)))

        return df

    def rename_columns(df):
        column_mapping = {
            0: "REG",
            1: "IND_OPER",
            2: "IND_EMIT",
            3: "COD_PART",
            4: "COD_MOD",
            5: "COD_SIT",
            6: "SER",
            7: "NUM_DOC",
            8: "CHV_NFE",
            9: "DT_DOC",
            10: "DT_E_S",
            11: "VL_DOC",
            12: "IND_PGTO",
            13: "VL_DESC",
            14: "VL_ABAT_NT",
            15: "VL_MERC",
        }

        c170_column_mapping = {
            30: "REG_C170",
            31: "NUM_ITEM",
            32: "COD_ITEM",
            33: "DESCR_PRODUTO",
            34: "QTD",
            35: "UN",
            36: "VL_ITEM",
            37: "VL_DESC2",
            38: "IND_MOV",
            39: "CST_ICMS",
            40: "CFOP",
            41: "COD_NAT",
            42: "VL_BC_ICMS",
            43: "ALIQ_ICMS",
            44: "VL_ICMS",
            45: "VL_BC_ICMS_ST",
        }

        for column, name in column_mapping.items():
            df.rename(columns={column: name}, inplace=True)

        for column, name in c170_column_mapping.items():
            if column in df.columns:
                df.rename(columns={column: name}, inplace=True)

        return df

    st.title("Extrator de Registros C100 e C170")

  uploaded_files = st.file_uploader("Selecione um ou mais arquivos EFD (TXT e Latin-1):", type="txt", accept_multiple_files=True)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        file_bytes = io.BytesIO(uploaded_file.getbuffer())
        file_text = file_bytes.read().decode("latin-1")
        file_lines = file_text.splitlines()
        df_combined = extract_records(file_lines, "latin-1")
        df_combined = rename_columns(df_combined)

        st.write(f"Registros C100 e C170 do arquivo {uploaded_file.name} com identificação do registro na primeira coluna e colunas renomeadas:")
        st.write(df_combined)

        if st.button(f"Exportar CSV do arquivo {uploaded_file.name} separado por '|'"):
            # Exporta o dataframe como um arquivo CSV separado por ';'
            csv = df_combined.to_csv(index=False, sep="|", encoding="utf-8-sig")
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{uploaded_file.name}.csv">Download do arquivo CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

