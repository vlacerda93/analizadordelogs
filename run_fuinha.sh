#!/usr/bin/env bash
echo "========================================================"
echo "              FUINHA NETWORK MONITOR v4.0               "
echo "========================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não foi encontrado. Por favor instale o python3."
    exit 1
fi

echo "Verificando dependências..."
pip3 install -r requirements.txt --quiet

echo "Iniciando o Fuinha..."
cd ver3.0
if [ "$EUID" -ne 0 ]; then
    echo "Executando como superusuário (sudo) para captura de processos..."
    sudo python3 main.py
else
    python3 main.py
fi
