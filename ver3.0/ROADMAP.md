# 🦊 Fuinha - ROADMAP & Status do Projeto

Olá, Antigravity do futuro! Este arquivo foi criado em parceria com o **Vinicius** para garantir que você saiba exatamente onde paramos e qual é a visão deste projeto. 

**O Fuinha não é apenas um monitor de rede; é um "Tradutor de Internet" para usuários comuns.**

---

## ✅ O que já foi conquistado (v3.0 - Dia 1)

1.  **Interface Gráfica (Aesthetics First)**:
    -   Design **Deep Dark** moderno usando `customtkinter`.
    -   **Global Speed Header**: Blocos grandes de DOWNLOAD e UPLOAD em MB/s.
    -   **PieChart Widget**: Componente personalizado em `tkinter.Canvas` para exibir a distribuição de banda.
    -   **Tabela Simplificada**: Apenas Nome do Processo | Download | Upload (em KB/s).
    -   **Rodapé de Dicas**: "Dica do Fuinha" com insights dinâmicos e localização.

2.  **Motor (Monitor Engine)**:
    -   **Distribuição Ponderada**: Lógica para estimar KB/s por processo (já que o `psutil` não dá isso direto).
    -   **Identificação Inteligente**: Fallback para "Sistema / Outros" quando o tráfego não tem dono identificado.
    -   **Sensibilidade**: Ajustado para detectar pequenas mudanças na rede.

3.  **Localização (I18n)**:
    -   Sistema robusto de `json` para PT-BR e EN.
    -   Tratamento de erros quando o app não é rodado como Sudo/Admin no Linux.

4.  **Repositório e Docs**:
    -   Commits organizados, novo README conceitual e `.gitignore`.

---

## 🛠️ O que falta fazer (O Próximo Passo!)

- [ ] **Mapeamento de Nomes Amigáveis**:
    -   Criar um dicionário (ex: `PROCESS_NAMES_MAP`) para que `brave` apareça como `Navegador Brave`, `steam` como `Steam Store`, etc.
- [ ] **Geração de Instaladores (O Vinicius quer isso!)**:
    -   Finalizar a criação do `.deb` para Linux e `.exe` para Windows usando os arquivos na pasta `build_tools`.
- [ ] **Menu de Configurações Privado**:
    -   Uma pequena engrenagem para trocar idioma (PT/EN) e taxa de atualização sem fechar o app.
- [ ] **Modo Tray (Minimizar)**:
    -   Garantir que o ícone do sistema (assets/icon.png) apareça no tray e o app continue monitorando em segundo plano.
- [ ] **Histórico Curto**:
    -   Talvez um pequeno gráfico de linha para mostrar a velocidade dos últimos 60 segundos.

---

## 🧠 Notas para o Futuro Antigravity

-   **Vinicius** gosta de designs **Premium** e **Wowed**. Fuja do simples, foque no estético.
-   **No Linux**: O monitor de processos (`net_connections`) EXIGE `sudo`. Sempre lembre o Vinicius de rodar com `sudo python3 main.py`.
-   **Performance**: O PieChart foi feito em `Canvas` puro para ser leve. Mantenha essa filosofia de poucas dependências pesadas.

---
*Assinado: Antigravity & Vinicius - Março de 2026*
