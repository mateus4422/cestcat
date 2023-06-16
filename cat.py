import streamlit as st
import pandas as pd

def cat_detalhes():
    def get_cabecalho(registro):
        cabecalho = {
            '0000': ['REG', 'PERIODO', 'NOME', 'CNPJ', 'IE', 'COD_MUN', 'COD_VER', 'COD_FIN'],
            '0150': ['REG', 'COD_PART', 'NOME', 'COD_PAIS', 'CNPJ', 'CPF', 'IE', 'COD_MUN'],
            '0200': ['REG', 'COD_ITEM', 'DESCR_ITEM', 'COD_BARRA', 'UNID_INV', 'COD_NCM', 'ALIQ_ICMS', 'CEST'],
            '0220': ['REG', 'UNID_CONV', 'FAT_CONV'],
            '1050': ['REG','COD_ITEM','QTD_INI','ICMS_TOT_INI', 'QTD_FIM', 'ICMS_TOT_FIM'],
            '1100': ['REG', 'CHV_DOC', 'DATA', 'NUM_ITEM', 'IND_OPER', 'COD_ITEM', 'CFOP', 'QTD', 'ICMS_TOT', 'VL_CONFR', 'CD_LEGAL']
        }
        return cabecalho.get(registro, [])


    def get_texto_fixo(registro):
        texto_fixo = {
            '0000': 'Registro "0000": Abertura do Arquivo Digital e Identificação do Contribuinte\r\r'
                    '**REG**: Texto fixo contendo “0000”\r\r'
                    '**PERIODO**: Período das informações contidas no arquivo\r\r'
                    '**NOME**: Nome empresarial da entidade.\r\r'
                    '**CNPJ**: Número de inscrição da entidade no CNPJ.\r\r'
                    '**IE**: Inscrição Estadual da entidade.\r\r'
                    '**COD_MUN**: Código do município do domicílio fiscal da entidade, conforme a tabela IBGE\r\r'
                    '**COD_VER**: Código da versão do leiaute conforme a Tabela de Versão do Leiaute\r\r'
                    '**COD_FIN**: Código da finalidade do arquivo conforme a Tabela Finalidade de Entrega do Arquivo',
            '0150': 'Registro "0150": Tabela de Cadastro do Participante\r\r'
                    '**REG**: Texto fixo contendo “0150”\r\r'
                    '**COD_PART**: Código de identificação do participante no arquivo.\r\r'
                    '**NOME**: Nome pessoal ou empresarial do participante\n'
                    '**COD_PAIS**: Código do país do participante\r\r'
                    '**CNPJ**: CNPJ do participante.\r\r'
                    '**CPF**: CPF do participante\r\r'
                    '**IE**: Inscrição Estadual do participante.\r\r'
                    '**COD_MUN**: Código do município, conforme a tabela IBGE',
            '0200': 'Registro "0200": Identificação do Item\r\r'
                    '**REG**: Texto fixo contendo "0200"\r\r'
                    '**COD_ITEM**: Código do item\r\r'
                    '**DESCR_ITEM**: Descrição do item\r\r'
                    '**COD_BARRA**: Representação alfanumérica do código de barra do produto\r\r'
                    '**UNID_INV**: Unidade de medida utilizada na quantificação de estoques.\r\r'
                    '**COD_NCM**: Código da Nomenclatura Comum do MERCOSUL\r\r'
                    '**ALIQ_ICMS**: Alíquota de ICMS aplicável ao item nas operações internas\r\r'
                    '**CEST**: Código Especificador da Substituição Tributária',
            '0220': 'Registro "0220": Fator de Conversão de Unidade',
            '1050': 'Registro "1050": Registro de Saldos\r\r'
                    '**REG**: Texto fixo contendo "1050"\r\r'
                    '**QTD_INI**: Quantidade inicial do item no início do primeiro dia do período.\r\r'
                    '**COD_ITEM**: Código do item conforme Registro 0200\r\r'
                    '**ICMS_TOT_INI**: Valor inicial acumulado do total do ICMS suportado pelo contribuinte, relativamente ao item, no início do primeiro dia do período.\r\r'
                    '**QTD_FIM**: Quantidade final do item no final do último dia do período.\r\r'
                    '**ICMS_TOT_FIM**: Valor final acumulado do total do ICMS suportado pelo contribuinte, relativamente ao item, no início do primeiro dia do período.',
            '1100': 'Registro "1100": Registro de Documento Fiscal Eletrônico para Fins de Ressarcimento de Substituição Tributária – SP\r\r'
                    '**REG**: Texto fixo contendo "1100"\\r\r'
                    '**CHV_DOC**: Chave do Documento Fiscal Eletrônico\r\r'
                    '**DATA**: Data da entrada da mercadoria ou da saída\r\r'
                    '**NUM_ITEM**: Número sequencial do item no Documento Fiscal Eletrônico\r\r'
                    '**IND_OPER**: Indicador do tipo de operação:\r\r'
                    '   - 0: Entrada\r\r'
                    '   - 1: Saída\r\r'
                    '**COD_ITEM**: Código do item conforme Registro 0200\r\r'
                    '**CFOP**: Código Fiscal de Operação e Prestação\r\r'
                    '**QTD**: Quantidade do Item\r\r'
                    '**ICMS_TOT**: Valor total do ICMS suportado pelo contribuinte nas operações de entrada\r\r'
                    '**VL_CONFR**: Valor de confronto nas operações de saída\r\r'
                    '**COD_LEGAL**: Código de Enquadramento Legal da hipótese de Ressarcimento ou Complemento de ICMS ST'
        }
        return texto_fixo.get(registro, '')

    file = st.file_uploader("Selecione o arquivo TXT da CAT", type='txt')

    if file:
        content = file.read().decode('utf-8')

        # Separa as linhas do arquivo por quebra de linha
        lines = content.split('\n')

        # Obtém os registros únicos presentes no arquivo
        registros = set(line.split('|')[0] for line in lines)

        # Cria o filtro para selecionar um registro
        selected_registro = st.selectbox("Selecione um registro", ['Selecione um registro'] + list(registros))

        if selected_registro != 'Selecione um registro':
            # Cria um DataFrame vazio
            df = pd.DataFrame()

            for line in lines:
                fields = line.split('|')
                registro = fields[0]
                data = fields[1:]

                if registro == selected_registro:
                    # Cria uma lista que inclui o registro selecionado como o primeiro elemento
                    row = [selected_registro] + data

                    # Cria um DataFrame temporário com a linha de dados
                    temp_df = pd.DataFrame([row], columns=get_cabecalho(selected_registro))

                    # Concatena o DataFrame temporário com o DataFrame principal
                    df = pd.concat([df, temp_df], ignore_index=True)

            if len(df) > 0:
                # Exibe o DataFrame com o cabeçalho personalizado
                st.dataframe(df)

                # Obtém o texto fixo correspondente ao registro selecionado
                texto_fixo = get_texto_fixo(selected_registro)

                # Exibe o painel com o texto fixo
                st.subheader("Significado")
                st.markdown(texto_fixo)
            else:
                st.warning("Não foram encontrados dados para o registro selecionado.")
        else:
            st.info("Selecione um registro")

cat_detalhes()
