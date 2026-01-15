# Análise de Logs com python Ver2.1

Projeto em Bash para praticar análise básica de logs no Linux, com foco em estudos para SOC Analyst e blue team.

O objetivo é criar pequenos scripts que ajudem a:
- Contar erros, avisos e eventos importantes em arquivos de log.
- Identificar IPs mais frequentes.
- Praticar comandos clássicos de linha de comando como `grep`, `sort`, `uniq`, `head` e `wc`.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/vlacerda93/analise-de-logs-linux.git
   cd analise-de-logs-linux
   ```

2. Dê permissão de execução para o script:
   ```bash
   chmod +x scripts/analisar_logs.sh
   ```

3. Execute o script apontando para um arquivo de log:
   ```bash
   ./scripts/analisar_logs.sh logs-exemplo/access.log
   ```

## Funcionalidades (versão inicial)

- Mostrar o número total de linhas do log.
- Contar quantas linhas contêm as palavras `error` e `failed` (não sensível a maiúsculas/minúsculas).
- Listar os 5 IPs que mais aparecem no log (quando o log tiver IPs na primeira coluna).

Novas funcionalidades serão adicionadas à medida que o estudo avançar.

## Estrutura do projeto

```
analise-de-logs-linux/
├─ scripts/
│  └─ analisar_logs.sh       # Script principal de análise
├─ logs-exemplo/
│  └─ access.log             # Arquivo de log de exemplo para testar
└─ README.md                 # Este arquivo
```

## Roadmap

- [✓] Versão 1.0: Contagem básica de erros e IPs
- [✓] Versão 1.1: Adicionar filtro por data/hora
- [✓] Versão 1.2: Monitoramento de log em tempo real
- [✓] Versão 2.0: Exportar relatórios para arquivo

## Sobre

Projeto criado como parte dos estudos para SOC Analyst Level 1, seguindo o caminho de aprendizado do TryHackMe e conteúdos de  segurança cibernética com python e shell.
