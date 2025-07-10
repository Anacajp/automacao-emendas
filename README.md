# Automação de Atualização de Planilha via BI (Selenium + Google Sheets)

## Fluxo do Projeto

1. **Baixa o CSV** do BI usando Selenium (headless)
2. **Atualiza a planilha Google Sheets** com os dados do CSV
3. **Executa periodicamente** (pode ser agendado na nuvem)

## Configuração

- Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
- Ative a API do Google Sheets
- Gere e baixe o arquivo de credenciais JSON
- Defina as variáveis de ambiente:
  - `GOOGLE_CREDENTIALS_JSON`: caminho para o JSON de credenciais
  - `SHEET_ID`: ID da planilha Google
  - `SHEET_RANGE`: nome da aba (ex: 'Página1')
  - `URL_BI`: URL do BI
  - (Opcional) `BI_USER` e `BI_PASS` se precisar de login
  - (Opcional) `CSV_PATH` para definir onde salvar o CSV

## Instalação

```bash
pip install -r src/requirements.txt
```

## Execução

```bash
python src/main.py
```

## Observações

- Ajuste o código do Selenium conforme o BI utilizado (login, navegação, botão de exportação)
- Para rodar na nuvem, use Google Cloud Run, Functions ou uma VM com cron
- Adicione logs e monitore as execuções
