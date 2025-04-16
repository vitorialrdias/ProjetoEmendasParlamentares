from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import datetime
from dateutil.relativedelta import relativedelta


class Navegador:
    def __init__(self, url, login="", password=""):
        self.url = url
        self.login = login
        self.password = password
    
    def openPage(self) -> webdriver:

        options = Options()

        # Desativa pop-ups e cookies
        prefs = {
            "profile.default_content_setting_values.popups": 1,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get(self.url)

        # Aguardamos a div main-content carregar!
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='main-content']"))
        )

        return driver
    
    def navSite(self, driver) -> bool:
        try:
            # Inicia o processo de navegação pelo site
            driver.find_element(By.XPATH, "//button[@id='accept-all-btn' and contains(text(),'Aceitar todos')]").click()
            pular = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='modal-tutorial']/div/div/div/div/div[2]/div[2]/div/button"))
            )
            pular.click()

            link_emendas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h5[contains(text(),'Emendas Parlamentares')]/ancestor::div[contains(@class,'flipcard-wrap')]"))
            )
            driver.execute_script("arguments[0].click();", link_emendas)



            link_detalhada = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='button-consulta-emendas']"))
            )
            link_detalhada.click()

            link_por_emenda = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'related-topics-title') and contains(text(), 'Por Emenda Parlamentar')]"))
            )
            link_por_emenda.click()


            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


            return True

            driver.quit()
        except Exception as e:
            print(f"Erro ao navegar pelo site: {e}")
            return False
        
    def filtroPesquisa(self, driver) -> bool:
        try:
            # Inicia o processo de filtragem
            limpar_filtros = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnLimparFiltrosSumario']"))
            )

            limpar_filtros.click()

            btn_ano = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btn-ano-da-emenda-1']"))
            )

            btn_ano.click()

            ano_atual = datetime.datetime.now().year
            ano_referencia = (datetime.datetime.now() - relativedelta(years=1)).year

            filtrar_data_inicial = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='de']"))
            )

            filtrar_data_final = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='ate']"))
            )

            filtrar_data_inicial.send_keys(ano_referencia)
            filtrar_data_final.send_keys(ano_atual)


            btn_add = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='id-box-filtro']/div/div/ul/li[2]/div/div[1]/div/div/div[2]/button"))
            )
            driver.execute_script("arguments[0].click();", btn_add)

            filtrar_funcao = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='btn-funo-e-subfuno-8']"))
            )

            filtrar_funcao.click()
            time.sleep(5)

            filtrar_funcao_edu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='token-input-funcaoSubfuncao']"))
            )
            filtrar_funcao_edu.send_keys('Educação')

            option_edu = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, "//li[contains(@class, 'token-input-dropdown-item2')]//b[normalize-space()='Educação']"))
            )

            option_edu.click()

            driver.execute_script("arguments[0].click();", btn_add)

            btn_consultar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='id9']/div[2]/div[1]/button"))
            )
            btn_consultar.click()
            print('Filtragem de pesquisa efetuada com sucesso!')


            return True
        except Exception as e:
            print(f'Erro ao filtrar dados: {e}')
            return False
        
    
    def downloadArquivo(self, driver) -> bool:
        try:
            btn_cvs = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='btnBaixar']"))
            )
            btn_cvs.click()

            tempo_maximo = 15
            tempo_inicial = time.time()

            caminho_pasta = os.path.join(os.environ['USERPROFILE'], 'Downloads')
            nome_arquivo = "emendas"
            arquivo = (fr'{caminho_pasta}\{nome_arquivo}.csv')  


            while (not arquivo) and time.time() - tempo_inicial < tempo_maximo:
                time.sleep(1)

            return True
                
        except Exception as e:
            print(f'Erro ao baixar arquivo: {e}')
            return False