import os

# Caminho onde o XLSX será salvo temporariamente
default_xlsx_path = os.path.join(os.path.dirname(__file__), '..', 'dados_bi.xlsx')
XLSX_PATH = os.environ.get('XLSX_PATH', default_xlsx_path)

# ID da planilha Google Sheets (pegar na URL da planilha)
SHEET_ID = os.environ.get('SHEET_ID', 'COLOQUE_O_ID_AQUI')

# Nome da aba ou range (ex: 'Página1')
SHEET_RANGE = os.environ.get('SHEET_RANGE', 'Página1') 