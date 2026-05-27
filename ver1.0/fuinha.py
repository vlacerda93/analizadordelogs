import customtkinter as ctk
import threading
import os
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
import re
from collections import Counter

# --- CONFIGURAÇÃO DO SERVIDOR (Ouvinte) ---
server = Flask(__name__)
CORS(server) # Isso permite que o site fale com o Python
LOG_FILE = "access.log"

@server.route('/log', methods=['POST'])
def receber_log():
    try:
        data = request.json
        ip_cliente = request.remote_addr
        horario = datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
        url = data.get('url', 'URL Desconhecida')
        
        # Cria a linha no formato que seu analisador já entende
        nova_linha = f'{ip_cliente} - - [{horario}] "GET {url} HTTP/1.1" 200 OK\n'
        
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(nova_linha)
            
        return {"status": "recebido"}, 200
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}, 500
    
def iniciar_servidor():
    # O host='0.0.0.0' permite que outros aparelhos (celular, tablet) enviem logs para o seu PC
    server.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# --- INTERFACE GRÁFICA ---
class FuinhaLive(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fuinha Edition - Warhammer Live Monitor")
        self.geometry("900x600")

        # Layout
        self.lbl = ctk.CTkLabel(self, text="Monitoramento em Tempo Real", font=("Arial", 20, "bold"))
        self.lbl.pack(pady=10)

        self.status_paine = ctk.CTkLabel(self, text="Servidor Ativo: ouvindo porta 5000...", text_color="green")
        self.status_paine.pack()

        self.btn_atualizar = ctk.CTkButton(self, text="Atualizar Lista de Acessos", command=self.carregar_logs)
        self.btn_atualizar.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=800, height=400, font=("Consolas", 12))
        self.textbox.pack(padx=20, pady=20)
        
        # Tags de cores (as que criamos ontem)
        self.textbox.tag_config("sucesso", foreground="#2EB82E")

    def carregar_logs(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            
            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")
            
            for linha in linhas:
                # Se for um acesso vindo do site (marcado com OK), fica verde
                if "200 OK" in linha:
                    self.textbox.insert("end", linha, "sucesso")
                else:
                    self.textbox.insert("end", linha)
            
            self.textbox.configure(state="disabled")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # 1. Lança o servidor em segundo plano
    threading.Thread(target=iniciar_servidor, daemon=True).start()
    
    # 2. Abre a interface
    app = FuinhaLive()
    app.mainloop()