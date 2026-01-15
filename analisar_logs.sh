#!/bin/bash

# Script simples para análise básica de logs em Linux
# Uso: ./analisar_logs.sh caminho/para/arquivo.log

ARQUIVO_LOG="$1"

if [ -z "$ARQUIVO_LOG" ]; then
  echo "Uso: $0 caminho/para/arquivo.log"
  exit 1
fi

if [ ! -f "$ARQUIVO_LOG" ]; then
  echo "Erro: arquivo '$ARQUIVO_LOG' não encontrado."
  exit 1
fi

echo "===== Análise de log ====="
echo "Arquivo: $ARQUIVO_LOG"
echo

# Total de linhas
TOTAL_LINHAS=$(wc -l < "$ARQUIVO_LOG")
echo "Total de linhas no log: $TOTAL_LINHAS"

# Contagem de erros (error / failed)
ERROS=$(grep -i "error" "$ARQUIVO_LOG" | wc -l)
FALHAS=$(grep -i "failed" "$ARQUIVO_LOG" | wc -l)

echo "Linhas contendo 'error' : $ERROS"
echo "Linhas contendo 'failed': $FALHAS"

echo

# Top 5 IPs (assumindo IP na primeira coluna)
echo "Top 5 IPs mais frequentes (se houver IPs no log):"
awk '{print $1}' "$ARQUIVO_LOG" | \
  grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | \
  sort | uniq -c | sort -nr | head -5
