import customtkinter as ctk
from customtkinter import CTkTabview
import tkinter as tk
from tkinter import filedialog, messagebox
import pystray
from PIL import Image, ImageDraw
import threading
import queue
import json
import locale
import sys
import os
from utils import get_asset_path
from log_analyzer import LogAnalyzer

class PieChart(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.data = {}
        self.colors = ["#00FFAA", "#FF8800", "#FFCC00", "#AA00FF", "#00AAFF", "#FF00AA"]

    def update_chart(self, data):
        self.data = data
        self.delete("all")
        if not data:
            self.create_text(self.winfo_width()/2, self.winfo_height()/2, text="No Data", fill="gray")
            return
        total = sum(data.values())
        if total == 0:
            self.create_text(self.winfo_width()/2, self.winfo_height()/2, text="No Traffic", fill="gray")
            return
        start_ang = 0
        cx, cy = self.winfo_width()/2, self.winfo_height()/2
        r = min(cx, cy) - 20
        for i, (name, val) in enumerate(data.items()):
            extent = (val / total) * 359.9
            color = self.colors[i % len(self.colors)]
            self.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_ang, extent=extent, fill=color, outline="#222222")
            start_ang += extent

class UIManager:
    def __init__(self, engine):
        self.engine = engine
        self.app = ctk.CTk()
        self.app.title("Fuinha v4.0")
        self.app.geometry("650x800")
        self.header_frame = None
        self.dl_block = None
        self.dl_val_label = None
        self.ul_block = None
        self.ul_val_label = None
        self.table_frame = None
        self.apps_textbox = None
        self.footer_frame = None
        self.tip_title = None
        self.insight_label = None
        self.tray_icon = None
        self.locales = {}
        self.pie_chart = None
        self.log_analyzer = LogAnalyzer()
        self.current_tip = ""
        self.log_file_path = ""
        self.tabview = None
        self.network_tab = None
        self.logs_tab = None
        self.log_results_text = None
        self.log_file_label = None
        ctk.set_appearance_mode("dark")
        self.language = "pt_BR"
        self._load_language()
        self.stats_queue = queue.Queue()
        self.app.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        self.setup_ui()
        self.engine.callback = self.update_stats
        self._schedule_queue_check()

    def _load_language(self):
        sys_lang = locale.getdefaultlocale()[0]
        if sys_lang and 'pt' in sys_lang.lower():
            self.language = "pt_BR"
        else:
            self.language = "en"
        self._apply_locale()

    def _apply_locale(self):
        path = get_asset_path(f'locales/{self.language}.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.locales = json.load(f)
            self.app.title(self.locales["title"])
        except:
            self.locales = {"title": "Fuinha v4.0"}

    def setup_ui(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.app.title(self.locales["title"])
        self.tabview = CTkTabview(self.app)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.network_tab = self.tabview.add(self.locales.get("active_apps", "Monitor Rede"))
        self.logs_tab = self.tabview.add(self.locales.get("logs_tab", "Logs"))
        self.setup_network_tab()
        self.setup_logs_tab()
        self.setup_footer()

    def setup_network_tab(self):
        # Headers
        self.header_frame = ctk.CTkFrame(self.network_tab, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)
        self.dl_block = ctk.CTkFrame(self.header_frame, fg_color="#1a1a1a", border_width=2, border_color="#00FFAA")
        self.dl_block.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(self.dl_block, text=self.locales["download"] + " ⬇️", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FFAA").pack(pady=(10, 0))
        self.dl_val_label = ctk.CTkLabel(self.dl_block, text="0.0 Mbps", font=ctk.CTkFont(size=28, weight="bold"))
        self.dl_val_label.pack(pady=(0, 10))
        self.ul_block = ctk.CTkFrame(self.header_frame, fg_color="#1a1a1a", border_width=2, border_color="#FF8800")
        self.ul_block.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(self.ul_block, text=self.locales["upload"] + " ⬆️", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF8800").pack(pady=(10, 0))
        self.ul_val_label = ctk.CTkLabel(self.ul_block, text="0.0 Mbps", font=ctk.CTkFont(size=28, weight="bold"))
        self.ul_val_label.pack(pady=(0, 10))
        # Chart & Legend
        self.chart_container = ctk.CTkFrame(self.network_tab, fg_color="#1a1a1a", height=200)
        self.chart_container.pack(fill="x", pady=10, padx=20)
        self.chart_container.pack_propagate(False)
        self.pie_chart = PieChart(self.chart_container, bg="#1a1a1a", width=200, height=200)
        self.pie_chart.pack(side="left", padx=20)
        self.legend_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.legend_frame.pack(side="left", fill="both", expand=True)
        
        self.legend_rows = []
        for i in range(6):
            l_frame = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
            color_frame = ctk.CTkFrame(l_frame, width=12, height=12)
            color_frame.pack(side="left", padx=5)
            label = ctk.CTkLabel(l_frame, text="", font=ctk.CTkFont(size=12))
            label.pack(side="left")
            self.legend_rows.append((l_frame, color_frame, label))

        # Textbox
        self.apps_label = ctk.CTkLabel(self.network_tab, text=self.locales["active_apps"], font=ctk.CTkFont(size=16, weight="bold"))
        self.apps_label.pack(anchor="w", padx=20, pady=(20, 5))
        self.apps_textbox = ctk.CTkTextbox(self.network_tab, font=ctk.CTkFont(family="Consolas", size=13), height=200)
        self.apps_textbox.pack(fill="both", expand=True, padx=20, pady=5)

    def setup_logs_tab(self):
        title_label = ctk.CTkLabel(self.logs_tab, text="Auditoria de Segurança Local", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(self.logs_tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        btn_auth = ctk.CTkButton(btn_frame, text="Verificar Intrusões (Logs)", command=self.run_auth_audit)
        btn_auth.pack(side="left", padx=10, expand=True)
        
        btn_ports = ctk.CTkButton(btn_frame, text="Detectar Portas Abertas", command=self.run_ports_audit)
        btn_ports.pack(side="left", padx=10, expand=True)
        
        # Results
        self.log_results_text = ctk.CTkTextbox(self.logs_tab, font=ctk.CTkFont(family="Consolas", size=13), height=400)
        self.log_results_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_results_text.insert("0.0", "Clique em um dos botões acima para iniciar uma auditoria de segurança na máquina.")

    def setup_footer(self):
        self.footer_frame = ctk.CTkFrame(self.app, fg_color="#1a1a1a", height=100)
        self.footer_frame.pack(fill="x", padx=20, pady=10)
        self.footer_frame.pack_propagate(False)
        self.tip_title = ctk.CTkLabel(self.footer_frame, text="✨ Dica do Fuinha", font=ctk.CTkFont(size=14, weight="bold"), text_color="#AAAAAA")
        self.tip_title.pack(anchor="w", padx=15, pady=(10, 0))
        self.insight_label = ctk.CTkLabel(self.footer_frame, text="", font=ctk.CTkFont(size=13), wraplength=600, justify="left", text_color="#DDDDDD")
        self.insight_label.pack(anchor="w", padx=15, pady=5)

    def run_auth_audit(self):
        self.log_results_text.delete("0.0", "end")
        self.log_results_text.insert("0.0", "Analisando logs do sistema...\n")
        self.app.update()
        result = self.log_analyzer.check_auth_logs()
        self.log_results_text.delete("0.0", "end")
        self.log_results_text.insert("0.0", result)

    def run_ports_audit(self):
        self.log_results_text.delete("0.0", "end")
        self.log_results_text.insert("0.0", "Mapeando portas abertas...\n")
        self.app.update()
        result = self.log_analyzer.check_open_ports()
        self.log_results_text.delete("0.0", "end")
        self.log_results_text.insert("0.0", result)

    def _schedule_queue_check(self):
        try:
            while not self.stats_queue.empty():
                stats = self.stats_queue.get_nowait()
                self.update_network_tab(stats)
        except Exception:
            pass
        self.app.after(500, self._schedule_queue_check)

    def update_stats(self, stats):
        self.stats_queue.put(stats)

    def update_network_tab(self, stats):
        # Headers
        self.dl_val_label.configure(text=f"{stats['total_dl_mb']:.1f} Mbps")
        self.ul_val_label.configure(text=f"{stats['total_ul_mb']:.1f} Mbps")
        # Insight
        new_tip = self.locales.get(stats['insight'], stats['insight'])
        if new_tip != self.current_tip:
            self.current_tip = new_tip
            self.insight_label.configure(text=new_tip)
        # Apps list & chart
        self.apps_textbox.configure(state="normal")
        self.apps_textbox.delete("1.0", "end")
        
        apps = stats['apps']
        if not apps:
            self.apps_textbox.insert("end", self.locales["insight_no_admin"])
            self.pie_chart.update_chart({})
            for l_frame, _, _ in self.legend_rows:
                l_frame.pack_forget()
        else:
            sorted_apps = sorted(apps.items(), key=lambda x: (x[1]['dl_kb'] + x[1]['ul_kb']), reverse=True)
            top_apps = {name: data['dl_kb'] + data['ul_kb'] for name, data in sorted_apps[:5] if data['dl_kb'] + data['ul_kb'] > 0}
            self.pie_chart.update_chart(top_apps)
            for i, (app, data) in enumerate(sorted_apps):
                dl_val = f"{data['dl_kb']:.1f}"
                ul_val = f"{data['ul_kb']:.1f}"
                line = f"{app:<25} DL:{dl_val:>6} UL:{ul_val:>6}\n"
                self.apps_textbox.insert("end", line)
            
            for i, (l_frame, color_frame, label) in enumerate(self.legend_rows):
                if i < len(sorted_apps) and i < 6:
                    app_name = sorted_apps[i][0]
                    color = self.pie_chart.colors[i % len(self.pie_chart.colors)]
                    color_frame.configure(fg_color=color)
                    label.configure(text=app_name)
                    l_frame.pack(fill="x", pady=2)
                else:
                    l_frame.pack_forget()
                    
        if stats.get('suspicious'):
            self.apps_textbox.insert("end", "\n--- ⚠️ AVISO DE SEGURANÇA ---\n")
            for s in stats['suspicious']:
                self.apps_textbox.insert("end", f"Conexão suspeita: {s['app']} -> {s['ip']}\n")
                
        self.apps_textbox.configure(state="disabled")

    # Tray & other methods same as original (create_image, set_language_en/pt, init_tray, etc.)
    # ... (omit for brevity, copy from original)

    def set_language_en(self, icon, item):
        self.language = "en"
        self._apply_locale()
        try:
            self.tabview.set(self.network_tab, self.locales["active_apps"])
            self.tabview.set(self.logs_tab, self.locales["logs_tab"])
        except:
            pass

    def set_language_pt(self, icon, item):
        self.language = "pt_BR"
        self._apply_locale()
        self.tabview.set(self.network_tab, self.locales["active_apps"])
        self.tabview.set(self.logs_tab, self.locales["logs_tab"])

    # Copy other methods: create_image, init_tray, withdraw_window, show_window, quit_window, run from original
    def create_image(self):
        path = get_asset_path('assets/icon.png')
        try:
            if os.path.exists(path):
                return Image.open(path)
        except:
            pass
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 64, 64), radius=16, fill=(0, 200, 100))
        draw.text((22, 10), "F", fill="white")
        return image

    def init_tray(self):
        try:
            image = self.create_image()
            menu = pystray.Menu(
                pystray.MenuItem(self.locales.get("dashboard", "Dashboard"), self.show_window, default=True),
                pystray.MenuItem(self.locales.get("language", "Idioma"), pystray.Menu(
                    pystray.MenuItem("English", self.set_language_en),
                    pystray.MenuItem("Português", self.set_language_pt)
                )),
                pystray.MenuItem(self.locales.get("exit", "Sair"), self.quit_window)
            )
            title = self.locales.get("title", "Fuinha v4.0")
            self.tray_icon = pystray.Icon("Fuinha", image, title, menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except Exception as e:
            print(f"Aviso Tray Icon: {e}")

    def withdraw_window(self):
        self.app.withdraw()

    def show_window(self, icon=None, item=None):
        self.app.deiconify()
        self.app.lift()
        self.app.focus_force()

    def quit_window(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.engine.stop()
        self.app.quit()

    def run(self):
        self.engine.start()
        try:
            self.init_tray()
        except Exception as e:
            print(f"Erro ao inicializar tray: {e}")
        self.app.deiconify()
        self.app.lift()
        self.app.focus_force()
        self.app.attributes('-topmost', True)
        self.app.after(500, lambda: self.app.attributes('-topmost', False))
        self.app.mainloop()
