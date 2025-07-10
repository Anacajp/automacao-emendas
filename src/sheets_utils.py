import os
import csv
import gspread
from google.oauth2.service_account import Credentials

def atualizar_planilha_google(caminho_csv, sheet_id, sheet_name):
    """
    Atualiza a aba sheet_name da planilha Google Sheets com os dados do CSV.
    """
    creds = Credentials.from_service_account_file(os.environ.get('GOOGLE_CREDENTIALS_JSON'))
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.worksheet(sheet_name)

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))

    worksheet.clear()
    worksheet.update('A1', reader) 