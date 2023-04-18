import os
import pandas as pd
import streamlit as st
import base64

def save_uploaded_files(uploaded_files):
    file_paths = []
    for file in uploaded_files:
        with open(os.path.join('temp', file.name), 'wb') as f:
            f.write(file.getvalue())
        file_paths.append(os.path.join('temp', file.name))
    return file_paths


def load_data(file_paths):
    data = {}
    for file_path in file_paths:
        sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        data[file_path] = sheets
    return data


def get_file_date(file_name):
    date_str = file_name.split('.')[0]
    date_str = date_str.replace('.', '/')
    try:
        date = pd.to_datetime(date_str, format='%d/%m/%Y').date()
    except ValueError:
        date = None
    return date


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
        final_df[['MVA ST 1', 'aliquota']] /= 100
        final_df[['MVA ST 1', 'aliquota']] = final_df[['MVA ST 1', 'aliquota']].applymap('{:.2%}'.format)
        final_df = final_df[['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']]
        return final_df
    else:
        columns = ['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']
        return pd.DataFrame(columns=columns)

def get_file_date(file_name):
    date_str = file_name.split('.')[0]
    date_str = date_str.replace('.', '/')
    try:
        date = pd.to_datetime(date_str, format='%d/%m/%Y').date()
    except ValueError:
        date = None
    return date


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
        final_df[['MVA ST 1', 'aliquota']] /= 100
        final_df[['MVA ST 1', 'aliquota']] = final_df[['MVA ST 1', 'aliquota']].applymap('{:.2%}'.format)
        final_df = final_df[['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']]
        return final_df
    else:
        columns = ['Data', 'Categoria', 'CEST', 'MVA ST 1', 'aliquota']
        return pd.DataFrame(columns=columns)


st.title("Pesquisa de CEST")

uploaded_files = st.file_uploader("Selecione os arquivos xlsx", type=["xlsx"], accept_multiple_files=True)
if uploaded_files:
    file_paths = save_uploaded_files(uploaded_files)
    data = load_data(file_paths)

    cest_code = st.text_input("Digite o código CEST")
    if st.button("Pesquisar"):
        search_result = search_cest(data, cest_code)
        st.dataframe(search_result)
        csv = search_result.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="resultado.csv">Exportar resultado</a>'
        st.markdown(href, unsafe_allow_html=True)# Se a pasta contém arquivos
if arquivos:
    st.write("Arquivos encontrados na pasta:")
    for arquivo in arquivos:
        st.write("- " + os.path.basename(arquivo))

    # Executa a remoção do registro 0220 para cada arquivo
    if st.button("Remover registro 0220"):
        mudancas = []
        possui_0220 = False
        for arquivo in arquivos:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                with open(arquivo, 'rb') as f:
                    tmp_file.write(f.read())
                caminho_arquivo = tmp_file.name
                existe_0220, linhas_removidas, linhas_antigas, linhas_novas = remove_registro0220(caminho_arquivo)
                if existe_0220:
                    mudancas.append((arquivo, linhas_removidas, linhas_antigas, linhas_novas))
                possui_0220 = possui_0220 or existe_0220

        if possui_0220:
            st.write("Registro 0220 removido com sucesso!")
            # Exibindo mudanças em uma tabela
            if mudancas:
                df = pd.DataFrame(columns=['Arquivo', 'Linhas removidas', 'Linhas antigas', 'Linhas novas'])

                # Define as colunas do DataFrame
                df['Arquivo'] = [mudanca[0] for mudanca in mudancas]
                df['Linhas removidas'] = [mudanca[1] for mudanca in mudancas]
                df['Linhas antigas'] = [mudanca[2] for mudanca in mudancas]
                df['Linhas novas'] = [mudanca[3] for mudanca in mudancas]

                st.write("Mudanças realizadas:")
                st.write(df)

                # Atualiza a lista de arquivos
                arquivos = [os.path.join(caminho_pasta, arquivo) for arquivo in os.listdir(caminho_pasta) if
                            arquivo.endswith('.txt')]
                st.write("Arquivos atualizados:")
                for arquivo in arquivos:
                    st.write("- " + os.path.basename(arquivo))

# Se a pasta não contém arquivos
else:
    st.write("Nenhum arquivo encontrado na pasta.")


st.sidebar.title("Menu de navegação")
opcao = st.sidebar.selectbox("Selecione a opção desejada:", ["Selecione um ou mais arquivos", "Remover registro 0220"])

  if opcao == "Selecione um ou mais arquivos":
st.title("Remoção de registro 0220 em arquivos EFD")
st.write("Selecione um ou mais arquivos para remover o registro 0220.")
caminho_pasta = st.text_input("Digite o caminho completo da pasta contendo os arquivos EFD:", value=".")
arquivos = [os.path.join(caminho_pasta, arquivo) for arquivo in os.listdir(caminho_pasta) if
arquivo.endswith('.txt')]

