import streamlit as st
import requests
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



# Diretório das imagens
diretoriodeimagens = 'Imagens/'
captcha1 = diretoriodeimagens + 'captcha01.png'

NOPECHA_KEY = 'sub_1N39yJCRwBwvt6ptc2ev7bCF'


def visualizacao_cf():
    st.title('Visualização de CF')
    cf_key = st.text_input("Digite a chave do CF", key="input_cf_visualizacao_cf")
    visualize_button = st.button('Visualizar CF')

    if visualize_button:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        with open('ext.crx', 'wb') as f:
            f.write(requests.get('https://nopecha.com/f/ext.crx').content)
        options.add_extension('ext.crx')

        servico - Service(ChromeDriverManager().install())
        driver - webdriver.Chrome(service=servico)
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://nopecha.com/setup#{NOPECHA_KEY}")
        driver.maximize_window()

        driver.get('https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx')
        time.sleep(4)

        driver.find_element(By.ID, 'details-button').click()
        time.sleep(0.5)
        driver.find_element(By.ID, 'proceed-link').click()
        time.sleep(1)

        campo_chave_acesso = driver.find_element(By.ID, 'conteudo_txtChaveAcesso')
        campo_chave_acesso.click()
        campo_chave_acesso.clear()
        driver.execute_script("arguments[0].value = arguments[1];", campo_chave_acesso, cf_key)
        time.sleep(0.5)

        while True:
            captcha = pyautogui.locateCenterOnScreen(captcha1, confidence=0.8)
            time.sleep(0.7)
            if captcha:
                print('Captcha verificado')
                driver.find_element(By.ID, 'conteudo_btnConsultar').click()
                break

                def check_refresh_key_event(event):
                    if event.event_type == 'down' and event.name == 'f5':  # Verifica se a tecla F5 foi pressionada
                        driver.refresh()  # Atualiza a página para fazer uma nova consulta

                # Captura o evento de pressionar a tecla F5
                keyboard.hook(check_refresh_key_event)

visualizacao_cf()
