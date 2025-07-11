import os
from selenium_utils import baixar_xlsx_bi
from sheets_utils import atualizar_planilha_google
from config import SHEET_ID
import logging

# Lista de seções: cada uma com URL, caminho do arquivo xlsx e nome da aba na planilha
SECOES = [
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2023-dep-estaduais/",
        "xlsx_path": "dados_2023.xlsx",
        "sheet_name": "VOLUNTÁRIAS - 2023"
    },
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2024-dep-estaduais/",
        "xlsx_path": "dados_2024.xlsx",
        "sheet_name": "VOLUNTÁRIAS - 2024"
    },
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2025-dep-estaduais/",
        "xlsx_path": "dados_2025.xlsx",
        "sheet_name": "VOLUNTÁRIAS - 2025"
    },
    {
        "url": "https://www.governo.sp.gov.br/loa-2025-emendas-impositivas/",
        "xlsx_path": "impositivas_2025.xlsx",
        "sheet_name": "IMPOSITIVAS - 2025"
    },
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    for secao in SECOES:
        logging.info(f"Processando seção: {secao['url']}")
        try:
            caminho_arquivo = baixar_xlsx_bi(secao["url"], secao["xlsx_path"], indice_botao=4)
            logging.info(f"Arquivo baixado: {caminho_arquivo}")
        except Exception as e:
            logging.error(f"Erro ao baixar arquivo da seção {secao['url']}: {e}")
            continue
        try:
            atualizar_planilha_google(caminho_arquivo, SHEET_ID, secao["sheet_name"])
            logging.info(f"Planilha atualizada: {secao['sheet_name']}")
        except Exception as e:
            logging.error(f"Erro ao atualizar planilha na aba {secao['sheet_name']}: {e}")
            continue
    logging.info('Automação finalizada.')

if __name__ == '__main__':
    main()
