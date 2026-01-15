import customtkinter as ctk
from collections import Counter
import re
import os
from tkinter import filedialog
import matplotlib.pyplot as plt # Importando a biblioteca de gráficos

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LogAnalyzerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analisador de Logs - Fuinha Edition Pro + Gráficos")
        self.geometry("1000x750")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_menu = ctk.CTkLabel(self.sidebar, text="MENU", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_menu.pack(pady=20)

        self.btn_carregar = ctk.CTkButton(self.sidebar, text="Analisar access.log", command=self.processar_log)
        self.btn_carregar.pack(pady=10, padx=20)

        self.btn_grafico = ctk.CTkButton(self.sidebar, text="Ver Gráfico de Horas", fg_color="purple", command=self.mostrar_grafico)
        self.btn_grafico.pack(pady=10, padx=20)

        self.btn_exportar = ctk.CTkButton(self.sidebar, text="Exportar Resumo", fg_color="green", command=self.exportar_resumo)
        self.btn_exportar.pack(pady=10, padx=20)

        # --- Área Principal ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.stats_label = ctk.CTkLabel(self.main_frame, text="Aguardando análise...", justify="left", anchor="w", font=("Segoe UI", 13))
        self.stats_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="w")

        self.textbox = ctk.CTkTextbox(self.main_frame, font=("Consolas", 12))
        self.textbox.grid(row=1, column=0, sticky="nsew")
        
        # Tags de Cores
        self.textbox.tag_config("erro", foreground="#FF4B4B")
        self.textbox.tag_config("alerta", foreground="#FFA500")
        self.textbox.tag_config("sucesso", foreground="#2EB82E")

        self.dados_grafico = Counter() # Guarda as horas para o gráfico

    def processar_log(self):
        caminho_diretorio = os.path.dirname(os.path.abspath(__file__))
        caminho_log = os.path.join(caminho_diretorio, "access.log")

        try:
            with open(caminho_log, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")

            # Resetar dados do gráfico
            self.dados_grafico = Counter()
            
            # Regex para pegar a hora (ex: :12:00:10 vira 12h)
            regex_hora = r':(\d{2}):\d{2}:\d{2}'

            for linha in linhas:
                # Extração de hora para o gráfico 
                hora_match = re.search(regex_hora, linha)
                if hora_match:
                    hora = hora_match.group(1)
                    self.dados_grafico[hora] += 1

                # Lógica de Cores 
                l_lower = linha.lower()
                tag = None
                if any(x in l_lower for x in ["error", "500", "failed"]): tag = "erro"
                elif any(x in l_lower for x in ["denied", "403", "401"]): tag = "alerta"
                elif " 200 " in l_lower or "success" in l_lower: tag = "sucesso"
                
                self.textbox.insert("end", linha, tag)

            self.textbox.configure(state="disabled")
            self.stats_label.configure(text=f"Análise Concluída! {len(linhas)} linhas processadas.\nClique em 'Ver Gráfico' para análise temporal.")

        except Exception as e:
            self.stats_label.configure(text=f"Erro: {e}")

    def mostrar_grafico(self):
        if not self.dados_grafico:
            return
        
        # Ordenar as horas para o gráfico ficar bonito
        horas_ordenadas = sorted(self.dados_grafico.keys())
        valores = [self.dados_grafico[h] for h in horas_ordenadas]

        plt.figure(figsize=(10, 5))
        plt.bar(horas_ordenadas, valores, color='skyblue')
        plt.title('Volume de Logs por Hora do Dia')
        plt.xlabel('Hora (H)')
        plt.ylabel('Quantidade de Eventos')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    def exportar_resumo(self):
        # ... (mesma lógica anterior) ...
        pass

if __name__ == "__main__":
    app = LogAnalyzerGUI()
    app.mainloop()