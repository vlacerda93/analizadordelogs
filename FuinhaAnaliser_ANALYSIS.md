# Análise do Projeto FuinhaAnaliser

## Visão Geral
O projeto **FuinhaAnaliser** é uma ferramenta de monitoramento e análise de rede/logs para Linux, evoluindo de um analisador básico de logs (ver1.0) para um monitor em tempo real de uso de internet (ver3.0). Foca em identificar apps consumindo rede, com UI gráfica (CustomTkinter). Suporta múltiplos idiomas (pt_BR/en), ícone na bandeja e builds multiplataforma.

## ver1.0: Analisador de Logs Básico (Incompleto)
- **Propósito**: Parse de logs Apache-like (ex: access.log com IPs, timestamps, status codes, erros como 401/500).
- **Componentes**:
  | Arquivo | Descrição |
  |---------|-----------|
  | `analisar_logs.sh` / `scripts/analisar_logs.sh` | Script Bash: Conta linhas, top 5 IPs, erros (`error`/`failed`), eventos. Uso: `./analisar_logs.sh access.log`. |
  | `fuinha.py` | Servidor Flask (`/log` POST recebe logs de dispositivos), salva em `access.log`. UI CustomTkinter: Botão \"Atualizar Lista de Acessos\", lista logs. Host `0.0.0.0:5000` para rede local. |
  | `logs-exemplo/access.log` | Exemplo com acessos simulados (IPs como 192.168.0.10, erros login/admin). |
  | `README.md` | Roadmap incompleto (filtros data, real-time, export). |
- **Limitações**: Básico, não real-time avançado, UI simples sem gráficos.

## ver3.0: Monitor de Uso de Rede (Atual, com Problemas de UI)
- **Propósito**: Monitora tráfego de rede em tempo real (download/upload KB/s), apps via `psutil.net_connections` (PID -> nome processo), insights/dicas. Gráfico pizza de top apps, lista conexões.
- **Arquitetura**:
  | Arquivo | Descrição |
  |---------|-----------|
  | `main.py` | Entry point: Inicia `NetworkMonitor` + `UIManager`. Checa admin, relança se preciso. |
  | `monitor_engine.py` | Thread daemon: Loop 1s atualiza `net_io_counters`, conexões inet, mapeia apps. Gera **tips aleatórios** (`random.choice(["insight_tip_1",...]`). Callback para UI. |
  | `ui_manager.py` | Dashboard CustomTkinter (450x600): Contadores velocidade, lista apps/conexões, **gráfico pizza** (`PieChart`) top 5 apps, legenda, footer com dica. Suporte bandeja (`pystray`), locales JSON. |
  | `utils.py` | Helpers: `is_admin()`, `run_as_admin()`. |
  | `ROADMAP.md` / `BUILD_GUIDE.md` | Planejamento builds. |
  | `build_tools/` | PyInstaller spec, Inno Setup (.iss), Debian control. |
  | `locales/*.json` | Textos pt_BR/en (ex: \"insight_no_admin\"). |
  | `assets/icon.png` | Ícone app. |
- **Funcionalidades**:
  - Velocidades DL/UL system-wide.
  - Top apps por conexões ativas (precisa sudo/root no Linux para PID mapping; senão modo \"No Admin\").
  - Pie chart + legenda dinâmica.
  - Dicas/insights no footer (ex: aleatórias ou baseadas em uso).
  - Tray icon para minimizar.

## Problemas Identificados na v3.0 (Causa dos \"Piscando\")
1. **Gráfico Pizza e Nomes de Softwares Piscando**:
   - `ui_manager.py::update_stats` -> `app.after(0, self.setup_ui())` **recrie UI inteira** todo ciclo (1s): Destroi/recrie `chart_container`, `pie_chart.update_chart(top_apps)`, legenda.
   - Causa flicker: Widgets recriados, não atualizados in-place.

2. **Dicas Alteram Muito Rápido**:
   - `monitor_engine.py::_generate_insight`: `random.choice(tips)` **nova dica toda iteração** (1s). Não cache/persistente.

3. **Outros**:
   - Sem merge com logs v1.0.
   - Dependências: psutil, customtkinter, matplotlib (pie), pystray, flask(? legado).
   - Linux precisa sudo para apps precisos.

## O Que Pode Ser Feito (Sugestões para v4.0)
1. **Fix UI Flicker**:
   - Atualizar **dados apenas** no pie chart/legenda/lista, sem recriar frames/widgets.
   - Usar `after(1000, self.update_loop)` otimizado.

2. **Melhorar Dicas**:
   - **Persistir dica** por X ciclos ou baseado em thresholds reais (ex: \"Chrome usa 80% banda\" -> dica específica).

3. **Merge v1.0 + v3.0**:
   - **Analisar logs + rede**: Widget aba para upload/parse access.log (IPs top, erros), integrado com monitor live.
   - Relatórios: Export JSON/CSV de sessões.

4. **Melhorias**:
   | Feature | Prioridade | Descrição |
   |---------|------------|-----------|
   | Throttling UI | Alta | Update 2-5s ao invés 1s. |
   | Gráficos Histórico | Média | Linha tempo uso (matplotlib). |
   | Filtros Logs | Alta | Data, IP, erro; real-time tail -f. |
   | Alertas | Média | Notifs se app > threshold. |
   | Multi-plataforma | Baixa | Fix Windows admin. |
   | Themes/Dark Mode | Baixa | Já CTk partial. |

## Dependências Prováveis (de imports)
```
pip install psutil customtkinter matplotlib pystray flask
```

## Como Rodar v3.0
```bash
cd ver3.0
python main.py  # Pode pedir sudo
```

Projeto bem estruturado, foco SOC/blue team. Próximos passos: Fix UI + merge logs!
