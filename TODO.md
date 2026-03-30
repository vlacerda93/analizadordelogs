# TODO - Evolução FuinhaAnaliser v4.0 (Merge Logs + Fixes)

## Status: [Em Progresso]

### 1. ✅ Criar arquivos/plano
- [x] FuinhaAnaliser_ANALYSIS.md
- [x] TODO.md

### 2. 🔄 Preparação (Procurar/criar arquivos)
- [x] Ler/corrigir arquivos chave v3.0 (main.py, ui_manager.py, etc.)
- [x] Criar `ver3.0/log_analyzer.py`
- [x] Atualizar locales pt_BR.json + en.json

### 3. 🛠️ Implementar Features
#### A. Fix Bugs v3.0
- [ ] ui_manager.py: Adicionar CTkTabview; setup_ui() só uma vez; novo `update_dashboard(stats)` (update labels/chart/text sem recriar).
- [ ] monitor_engine.py: Insights lógicos (não random); throttle 2s; persist tip 10s.
#### B. Nova Aba Logs
- [ ] ui_manager.py: Aba \"Analisador de Logs\" com file dialog, textbox resultados, botões Analyze/Export CSV, live tail checkbox.
- [ ] log_analyzer.py: Funções parse_log(file): top_ips, erros count, filter data/IP; tail live.
#### C. Melhorias Extras (Sugestões)
- [ ] Alertas: Threshold uso (ex: >10MB/s beep/notif).
- [ ] Histórico: Linha gráfico rede (5min history).
- [ ] Locales: pt_BR/en strings novas.

### 4. 📝 Atualizações Aux
- [ ] locales/pt_BR.json + en.json (abas, btns, alerts).
- [ ] ROADMAP.md: v4.0 done.

### 5. 🧪 Test & Build
- [ ] `cd ver3.0 && sudo python main.py`: No flicker, aba Logs funciona (test com ver1.0/access.log).
- [ ] Builds: PyInstaller/Debian.

**Comandos úteis**: `cat TODO.md | grep -v "✅\|🔄" | head -5`

