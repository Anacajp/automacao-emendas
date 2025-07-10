from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import logging

def baixar_csv_bi(url, caminho_csv, indice_botao=2):
    """
    Acessa a URL, encontra todos os elementos com a classe 'ui-role-button-fill',
    clica no elemento de índice especificado e salva o CSV no caminho_csv.
    Adiciona logs detalhados para acompanhamento.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    prefs = {"download.default_directory": os.path.dirname(os.path.abspath(caminho_csv))}
    chrome_options.add_experimental_option("prefs", prefs)

    logging.info(f"Iniciando Selenium para URL: {url}")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        logging.info("Página carregada. Aguardando elementos...")
        time.sleep(10)  # Aguarda carregar

        # Busca todos os elementos <path> com a classe desejada
        botoes = driver.find_elements("xpath", "//path[contains(@class, 'ui-role-button-fill')]")
        logging.info(f"Encontrados {len(botoes)} elementos com a classe 'ui-role-button-fill'.")

        if len(botoes) > indice_botao:
            logging.info(f"Clicando no elemento de índice {indice_botao}.")
            botoes[indice_botao].click()
            logging.info("Clique realizado. Aguardando download...")
            time.sleep(10)  # Aguarda download
        else:
            logging.error(f"Índice {indice_botao} fora do range. Apenas {len(botoes)} elementos encontrados.")
            raise Exception(f"Índice {indice_botao} fora do range dos elementos encontrados.")

        # (Opcional) Renomeie/mova o arquivo baixado para caminho_csv se necessário
        # Dependendo do site, pode ser necessário identificar o nome do arquivo baixado
        # Exemplo:
        # downloads = os.listdir(os.path.dirname(os.path.abspath(caminho_csv)))
        # arquivo_baixado = max([os.path.join(..., f) for f in downloads], key=os.path.getctime)
        # os.rename(arquivo_baixado, caminho_csv)
        # Se o nome já for igual, não precisa mover
        logging.info("Processo de download finalizado.")
    except Exception as e:
        logging.error(f"Erro durante o processo de download: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Driver Selenium finalizado.") 


