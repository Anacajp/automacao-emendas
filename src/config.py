import os

# Caminho onde o CSV será salvo temporariamente
default_csv_path = os.path.join(os.path.dirname(__file__), '..', 'dados_bi.csv')
CSV_PATH = os.environ.get('CSV_PATH', default_csv_path)

# ID da planilha Google Sheets (pegar na URL da planilha)
SHEET_ID = os.environ.get('SHEET_ID', 'COLOQUE_O_ID_AQUI')

# Nome da aba ou range (ex: 'Página1')
SHEET_RANGE = os.environ.get('SHEET_RANGE', 'Página1') 