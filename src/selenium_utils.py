from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob

def baixar_xlsx_bi(url, caminho_xlsx, indice_botao=4):
    """
    Acessa a URL, entra no iframe do dashboard, tenta clicar na div mãe do botão 'Baixar os dados' usando data-testid ou classes.
    Espera ativamente pelo download do arquivo XLSX, renomeia/move para o nome esperado e retorna o caminho real do arquivo baixado.
    Adiciona logs detalhados para acompanhamento.
    """
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Remova para diagnóstico visual
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    prefs = {"download.default_directory": os.path.dirname(os.path.abspath(caminho_xlsx))}
    chrome_options.add_experimental_option("prefs", prefs)

    logging.info(f"Iniciando Selenium para URL: {url}")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        logging.info("Página carregada. Aguardando elementos...")
        time.sleep(10)  # Aguarda carregar
        wait = WebDriverWait(driver, 30)

        # 1. Localiza e entra no iframe
        try:
            iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id=\"page\"]/div/div[2]/div/div[2]/div/iframe')))
            driver.switch_to.frame(iframe)
            logging.info("Entrou no iframe do dashboard Power BI.")
        except Exception as e:
            logging.error(f"Não foi possível localizar/entrar no iframe: {e}")
            raise

        divs = []
        # 2. Tenta pelo data-testid
        try:
            divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid=\"visual-content-desc\"]')))
            logging.info(f"Encontrados {len(divs)} divs com data-testid='visual-content-desc' dentro do iframe.")
        except Exception as e:
            logging.warning(f"Não encontrou divs por data-testid dentro do iframe: {e}")
        # 3. Se não encontrou, tenta pelas classes
        if not divs:
            try:
                divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.visual.customPadding.allow-deferred-rendering.visual-shape')))
                logging.info(f"Encontrados {len(divs)} divs pelas classes dentro do iframe.")
            except Exception as e:
                logging.error(f"Não encontrou divs pelas classes dentro do iframe: {e}")
                raise
        # 4. Tenta clicar no índice desejado
        if len(divs) > indice_botao:
            div_alvo = divs[indice_botao]
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", div_alvo)
                time.sleep(1)
                logging.info(f"Tentando clicar normalmente na div de índice {indice_botao} dentro do iframe.")
                wait.until(EC.element_to_be_clickable(div_alvo)).click()
                logging.info("Clique realizado na div mãe dentro do iframe. Aguardando download...")
                time.sleep(10)  # Aguarda download
            except Exception as e:
                logging.warning(f"Click normal falhou: {e}. Tentando via JavaScript...")
                try:
                    driver.execute_script("arguments[0].click();", div_alvo)
                    logging.info("Clique via JavaScript realizado na div mãe dentro do iframe. Aguardando download...")
                    time.sleep(10)
                except Exception as e2:
                    logging.error(f"Clique via JavaScript também falhou: {e2}. Tentando buscar filhos clicáveis...")
                    filhos = div_alvo.find_elements(By.XPATH, ".//button|.//a|.//svg|.//g")
                    for filho in filhos:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView(true);", filho)
                            time.sleep(0.5)
                            filho.click()
                            logging.info("Clique realizado em filho clicável da div mãe. Aguardando download...")
                            time.sleep(10)
                            break
                        except Exception as e3:
                            logging.warning(f"Clique em filho falhou: {e3}")
                    else:
                        logging.error("Nenhum filho clicável funcionou. Não foi possível clicar no botão de download.")
                        raise
        else:
            logging.error(f"Índice {indice_botao} fora do range. Apenas {len(divs)} divs encontradas dentro do iframe.")
            raise Exception(f"Índice {indice_botao} fora do range dos elementos encontrados dentro do iframe.")
        logging.info("Processo de clique na div mãe dentro do iframe finalizado.")

        # 5. Espera ativa pelo arquivo XLSX
        download_dir = os.path.dirname(os.path.abspath(caminho_xlsx))
        timeout = 40
        start_time = time.time()
        arquivo_baixado = None
        while time.time() - start_time < timeout:
            arquivos_xlsx = glob.glob(os.path.join(download_dir, "*.xlsx"))
            logging.info(f"Arquivos na pasta de download: {os.listdir(download_dir)}")
            if arquivos_xlsx:
                arquivo_baixado = max(arquivos_xlsx, key=os.path.getctime)
                if os.path.exists(arquivo_baixado):
                    break
            time.sleep(1)
        if not arquivo_baixado or not os.path.exists(arquivo_baixado):
            logging.error("Nenhum arquivo XLSX encontrado após o download!")
            raise Exception("Nenhum arquivo XLSX encontrado.")
        # Renomeia/move para o nome esperado, se necessário
        if arquivo_baixado != caminho_xlsx:
            os.rename(arquivo_baixado, caminho_xlsx)
            logging.info(f"Arquivo baixado renomeado/movido para: {caminho_xlsx}")
        else:
            logging.info("Arquivo baixado já está com o nome esperado.")
        logging.info(f"Arquivo baixado: {caminho_xlsx}")
        return caminho_xlsx
    except Exception as e:
        logging.error(f"Erro durante o processo de download: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Driver Selenium finalizado.") 


