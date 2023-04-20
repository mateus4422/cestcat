import streamlit as st
import pandas as pd
import base64
import os

def cest():
    def save_uploaded_files(uploaded_files):
        file_paths = []
        for file in uploaded_files:
            with open(os.path.join(file.name), 'wb') as f:
                f.write(file.getvalue())
            file_paths.append(os.path.join(file.name))
        return file_paths

    def load_data(file_paths):
        data = {}
        for file_path in file_paths:
            sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            data[file_path] = sheets
        return data

    def search_cest(data, cest_code):
        result = []
        for file_path, sheets in data.items():
            for sheet_name, df in sheets.items():
                matching_rows = df[df.apply(lambda row: row.astype(str).str.contains(cest_code).any(), axis=1)]
                if not matching_rows.empty:
                    matching_rows['Arquivo'] = os.path.basename(file_path)
                    matching_rows['CEST'] = cest_code
                    matching_rows['Categoria'] = sheet_name
                    result.append(matching_rows)

        if result:
            final_df = pd.concat(result, ignore_index=True)
            final_df['Data'] = final_df['Arquivo'].str.replace('.xlsx', '').str.replace('.', '/')
            final_df['Data'] = pd.to_datetime(final_df['Data'], format='%d/%m/%Y')
            final_df['MVA ST 1'] = final_df['Unnamed: 10'] * 100
            final_df['aliquota'] = final_df['Unnamed: 12'] * 100
            final_df = final_df[['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']]
            final_df = final_df.sort_values('Data', ascending=False)

            # Excluir linhas com valores iguais a zero nas colunas "MVA ST 1" e "aliquota"
            final_df = final_df[(final_df['MVA ST 1'] != 0) & (final_df['aliquota'] != 0)]

            final_df[['MVA ST 1', 'aliquota']] = final_df[['MVA ST 1', 'aliquota']] / 100
            final_df[['MVA ST 1', 'aliquota']] = final_df[['MVA ST 1', 'aliquota']].applymap('{:.2%}'.format)
            final_df = final_df[['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']]
            return final_df
        else:
            columns = ['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']
            return pd.DataFrame(columns=columns)
    def export_result(result_df):
        csv = result_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="resultado.csv">Exportar resultado</a>'
        st.markdown(href, unsafe_allow_html=True)


    st.write("Por favor, faça o upload dos arquivos que deseja pesquisar.")

    uploaded_files = st.file_uploader("Selecione os arquivos xlsx", type=["xlsx"], accept_multiple_files=True)
        if uploaded_files:
               file_paths = save_uploaded_files(uploaded_files)
        data = load_data(file_paths)

        cest_code = st.text_input("Digite o código CEST")
        if st.button("Pesquisar"):
            search_result = search_cest(data, cest_code)
            if not search_result.empty:
                st.dataframe(search_result)

                export_result(search_result)
            else:
                st.write("Nenhum resultado encontrado")

    st.write("Desenvolvido por [Mateus Ramos](https://www.linkedin.com/in/mateusramosb/)")  
