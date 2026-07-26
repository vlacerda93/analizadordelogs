# 🦡 Fuinha Network Monitor (v4.0)

**Monitor de tráfego de rede e analisador de logs em tempo real.**  
O Fuinha traduz os pacotes de dados da sua rede e mapeia diretamente quais aplicativos (Brave, Discord, IDE, etc.) estão consumindo sua banda.

---

## 📦 Pacotes e Pré-requisitos (Leve e Enxuto)

O Fuinha é extremamente leve e requer apenas **4 pacotes Python** para funcionar:
- **`psutil`**: Captura de métricas de rede e PIDs de processos.
- **`customtkinter`**: Interface gráfica moderna e responsiva em Dark Mode.
- **`pystray`**: Suporte à bandeja do sistema (System Tray).
- **`Pillow`**: Renderização do ícone oficial do Texugo do Mel.

> **Requisito do Sistema:** Python 3.10+ instalado no Windows ou Linux. *(No Windows, recomendado executar com permissões de Administrador para mapear todos os PIDs).*

---

## 🚀 Como Instalar e Rodar no Windows

### 1. Rodar Direto (1 Clique)
Dê um duplo clique no arquivo **`run_fuinha.bat`**. O script instala os 4 pacotes automaticamente e inicia o programa.

### 2. Gerar Executável (`.exe`) e Atalho no Menu Iniciar
Dê um duplo clique no arquivo **`build_installer.bat`**.
- Compila o aplicativo standalone **`dist/Fuinha.exe`** (funciona sem precisar de Python).
- Adiciona o atalho oficial com o ícone do Texugo do Mel no **Menu Iniciar do Windows** e na **Área de Trabalho**.
- Após a instalação, basta abrir o Menu Iniciar e digitar **`Fuinha`**.

### 3. Desinstalar Atalhos do Windows
Dê um duplo clique em **`uninstall_fuinha.bat`** para remover todos os atalhos criados.

---

## 🐧 Como Rodar no Linux

```bash
chmod +x run_fuinha.sh
./run_fuinha.sh
```

---

## 🔧 Execução Manual via Terminal

```bash
pip install -r requirements.txt
python ver3.0/main.py
```

---
*Developed by Fuinha Team - Translating your internet for you.*
