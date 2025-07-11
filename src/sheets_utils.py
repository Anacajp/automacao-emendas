import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import logging

def atualizar_planilha_google(caminho_arquivo, sheet_id, sheet_name):
    """
    Atualiza a aba sheet_name da planilha Google Sheets com os dados do arquivo XLSX.
    """
    if not caminho_arquivo.lower().endswith('.xlsx'):
        logging.error(f"Arquivo não é XLSX: {caminho_arquivo}")
        raise Exception("Somente arquivos XLSX são suportados!")

    creds = Credentials.from_service_account_file(os.environ.get('GOOGLE_CREDENTIALS_JSON'))
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.worksheet(sheet_name)

    logging.info(f"Lendo arquivo XLSX: {caminho_arquivo}")
    df = pd.read_excel(caminho_arquivo)
    dados = [df.columns.values.tolist()] + df.values.tolist()

    worksheet.clear()
    worksheet.update('A1', dados)
    logging.info(f"Planilha {sheet_name} atualizada com sucesso!") 