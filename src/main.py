import os
from selenium_utils import baixar_csv_bi
from sheets_utils import atualizar_planilha_google
from config import SHEET_ID
import logging

# Lista de seções: cada uma com URL, caminho do CSV e nome da aba na planilha
SECOES = [
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2023-dep-estaduais/",
        "csv_path": "dados_2023.csv",
        "sheet_name": "VOLUNTÁRIAS - 2023"
    },
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2024-dep-estaduais/",
        "csv_path": "dados_2024.csv",
        "sheet_name": "VOLUNTÁRIAS - 2024"
    },
    {
        "url": "https://www.governo.sp.gov.br/transferencias-voluntarias-2025-dep-estaduais/",
        "csv_path": "dados_2025.csv",
        "sheet_name": "VOLUNTÁRIAS - 2025"
    },
    {
        "url": "https://www.governo.sp.gov.br/loa-2025-emendas-impositivas/",
        "csv_path": "impositivas_2025.csv",
        "sheet_name": "IMPOSITIVAS - 2025"
    },
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    for secao in SECOES:
        logging.info(f"Processando seção: {secao['url']}")
        try:
            baixar_csv_bi(secao["url"], secao["csv_path"])
            logging.info(f"CSV baixado: {secao['csv_path']}")
        except Exception as e:
            logging.error(f"Erro ao baixar CSV da seção {secao['url']}: {e}")
            continue
        try:
            atualizar_planilha_google(secao["csv_path"], SHEET_ID, secao["sheet_name"])
            logging.info(f"Planilha atualizada: {secao['sheet_name']}")
        except Exception as e:
            logging.error(f"Erro ao atualizar planilha na aba {secao['sheet_name']}: {e}")
            continue
    logging.info('Automação finalizada.')

if __name__ == '__main__':
    main()
