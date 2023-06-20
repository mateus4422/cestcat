import streamlit as st
import pandas as pd
import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

NOPECHA_KEY = 'sub_1N39yJCRwBwvt6ptc2ev7bCF'
EXTENSION_PATH = 'ext.crx'

def download_cf():
    st.title('Download de CF')

    # Campo de Chave do CF
    st.subheader("Chave do CF")
    cf_key = st.text_input("Digite a chave do CF", key="input_cf_download")

    # Botão de Baixar CF
    if st.button("Baixar CF"):
        cf_key_message = ""

        if len(cf_key) != 44:
            if len(cf_key) > 44:
                cf_key_message = "Números a mais. Verifique se o campo contém 44 caracteres."
            else:
                cf_key_message = "Quantidade de caracteres inválida. Deve conter 44 caracteres."

        if cf_key_message:
            st.warning(cf_key_message)
        else:
            execute_webdriver(cf_key)

    # Campo de CNPJ
    st.subheader("CNPJ")
    cnpj = st.text_input("Digite o CNPJ", key="input_cnpj")

    # Botão de Copiar
    if st.button("Copiar"):
        # Mensagem de validação para o CNPJ
        if len(cnpj) == 14:
            pyperclip.copy(cnpj)
            st.success("CNPJ copiado com sucesso.")
        elif len(cnpj) < 14:
            st.warning("Faltando números. Verifique se o campo contém 14 caracteres numéricos.")
        elif len(cnpj) > 14:
            st.warning("Contém números a mais. Verifique se o campo contém exatamente 14 caracteres numéricos.")

    txt_file = st.file_uploader("Carregar arquivo TXT com as chaves dos CFs", type='txt')

    if txt_file is not None:
        content = txt_file.getvalue().decode()
        lines = content.split("\n")
        unique_cf_keys = list(set(lines))
        unique_cf_keys = [key for key in unique_cf_keys if key.strip()]  # Remove chaves vazias

        dataframe = create_dataframe(unique_cf_keys)
        dataframe['Status'] = ''
        st.dataframe(dataframe)

        duplicated_cf_keys = dataframe[dataframe.duplicated(subset='Chave do CF', keep=False)]['Chave do CF'].tolist()
        if duplicated_cf_keys:
            st.write("Chaves duplicadas encontradas:")
            st.write(duplicated_cf_keys)
            if st.button("Remover chaves duplicadas"):
                dataframe = dataframe.drop_duplicates(subset='Chave do CF')
                dataframe.reset_index(drop=True, inplace=True)
                st.dataframe(dataframe)

def create_dataframe(cf_keys):
    dataframe = pd.DataFrame({
        "Chave do CF": cf_keys
    })
    return dataframe

def execute_webdriver(chave_acesso):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_extension(EXTENSION_PATH)

    driver = webdriver.Chrome(options=options)
    driver.get('https://satsp.fazenda.sp.gov.br/COMSAT/Account/'
               'LoginSSL.aspx?ReturnUrl=%2fCOMSAT%2fPrivate%2fConsultaCfeSemErros%2fConsultarCfeSemErro.aspx')
    time.sleep(3)

    driver.find_element(By.ID, 'details-button').click()
    time.sleep(0.5)
    driver.find_element(By.ID, 'proceed-link').click()
    time.sleep(1)

    # Clicar em Contabilista
    contabilista_element = driver.find_element(By.ID, 'conteudo_rbtContabilista')
    contabilista_element.click()
    time.sleep(3)

    # Clicar no botão Certificado Digital
    certificado_element = driver.find_element(By.ID, 'conteudo_imgCertificado')
    certificado_element.click()
    time.sleep(3)

    # Aguardar a janela de seleção de certificados aparecer
    time.sleep(2)

    # Selecionar CNPJ
    driver.find_element(By.LINK_TEXT, 'Selecionar CNPJ').click()
    time.sleep(0.9)
    cnpj_contribuinte = st.text_input("Digite o CNPJ", key="input_cnpj")
    driver.find_element(By.ID, 'conteudo_txtCNPJ_ContribuinteNro').clear()
    driver.find_element(By.ID, 'conteudo_txtCNPJ_ContribuinteNro').send_keys(cnpj_contribuinte[:8])
    driver.find_element(By.ID, 'conteudo_txtCNPJ_ContribuinteFilial').clear()
    driver.find_element(By.ID, 'conteudo_txtCNPJ_ContribuinteFilial').send_keys(cnpj_contribuinte[-6:])
    time.sleep(3)
    driver.find_element(By.ID, 'conteudo_btnPesquisar').click()
    time.sleep(2)

    # Selecionar CNPJ encontrado
    driver.find_element(By.ID, 'conteudo_gridCNPJ_lnkCNPJ_0').click()
    time.sleep(2)

    # Passar o mouse sobre o elemento "Cupons"
    cupons_element = driver.find_element(By.LINK_TEXT, 'Cupons')
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(cupons_element).perform()
    time.sleep(2)

    # Clicar em "Consultar CFe sem Erros"
    driver.find_element(By.LINK_TEXT, 'Consultar CFe sem Erros').click()
    time.sleep(2)

    # Aguardar 2 segundos
    time.sleep(2)

    # Colar a chave de acesso
    campo_chave_acesso = driver.find_element(By.ID, 'conteudo_txtChaveAcesso')
    campo_chave_acesso.clear()
    campo_chave_acesso.click()
    pyperclip.copy(chave_acesso)
    campo_chave_acesso.send_keys(Keys.CONTROL + 'v')

    time.sleep(3)

    # Clicar em "Pesquisar"
    driver.find_element(By.ID, 'conteudo_btnPesquisar').click()
    time.sleep(3)

    try:
        driver.find_element(By.ID, 'conteudo_grvConsultaCfeSemErros_lkbDownloadXml_0').click()
        time.sleep(3)
        st.success("Download do CF concluído.")
    except NoSuchElementException:
        error_dialog = driver.find_element(By.ID, 'dialog-modal')
        if error_dialog.text == "Não existem dados para os parâmetros de busca informados.":
            st.warning("Chave Inexistente")
        else:
            st.warning("Tente Novamente")
        driver.find_element(By.XPATH, '//span[text()="Ok"]').click()
        time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    download_cf()
