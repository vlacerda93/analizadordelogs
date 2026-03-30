import customtkinter as ctk
from customtkinter import CTkTabview
import tkinter as tk
from tkinter import filedialog, messagebox
import pystray
from PIL import Image, ImageDraw
import threading
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
        self.app.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        self.setup_ui()
        self.engine.callback = self.update_stats

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
        ctk.CTkLabel(self.dl_block, text=self.locales["download"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FFAA").pack(pady=(10, 0))
        self.dl_val_label = ctk.CTkLabel(self.dl_block, text="0.0 MB/s", font=ctk.CTkFont(size=28, weight="bold"))
        self.dl_val_label.pack(pady=(0, 10))
        self.ul_block = ctk.CTkFrame(self.header_frame, fg_color="#1a1a1a", border_width=2, border_color="#FF8800")
        self.ul_block.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(self.ul_block, text=self.locales["upload"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF8800").pack(pady=(10, 0))
        self.ul_val_label = ctk.CTkLabel(self.ul_block, text="0.0 MB/s", font=ctk.CTkFont(size=28, weight="bold"))
        self.ul_val_label.pack(pady=(0, 10))
        # Chart & Legend
        self.chart_container = ctk.CTkFrame(self.network_tab, fg_color="#1a1a1a", height=200)
        self.chart_container.pack(fill="x", pady=10, padx=20)
        self.chart_container.pack_propagate(False)
        self.pie_chart = PieChart(self.chart_container, bg="#1a1a1a", width=200, height=200)
        self.pie_chart.pack(side="left", padx=20)
        self.legend_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.legend_frame.pack(side="left", fill="both", expand=True)
        # Textbox
        self.apps_label = ctk.CTkLabel(self.network_tab, text=self.locales["active_apps"], font=ctk.CTkFont(size=16, weight="bold"))
        self.apps_label.pack(anchor="w", padx=20, pady=(20, 5))
        self.apps_textbox = ctk.CTkTextbox(self.network_tab, font=ctk.CTkFont(family="Consolas", size=13), height=200)
        self.apps_textbox.pack(fill="both", expand=True, padx=20, pady=5)

    def setup_logs_tab(self):
        # File label
        self.log_file_label = ctk.CTkLabel(self.logs_tab, text=self.locales["log_no_file"])
        self.log_file_label.pack(pady=10)
        # Buttons frame
        btn_frame = ctk.CTkFrame(self.logs_tab)
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text=self.locales["choose_file"], command=self.choose_log_file).pack(side="left", padx=10)
        self.analyze_btn = ctk.CTkButton(btn_frame, text=self.locales["analyze_btn"], command=self.analyze_log, state="disabled")
        self.analyze_btn.pack(side="left", padx=10)
        self.export_btn = ctk.CTkButton(btn_frame, text=self.locales["export_csv"], command=self.export_log, state="disabled")
        self.export_btn.pack(side="left", padx=10)
        # Results
        self.log_results_text = ctk.CTkTextbox(self.logs_tab, height=400)
        self.log_results_text.pack(fill="both", expand=True, padx=20, pady=10)

    def setup_footer(self):
        self.footer_frame = ctk.CTkFrame(self.app, fg_color="#1a1a1a", height=100)
        self.footer_frame.pack(fill="x", padx=20, pady=10)
        self.footer_frame.pack_propagate(False)
        self.tip_title = ctk.CTkLabel(self.footer_frame, text="✨ Dica do Fuinha", font=ctk.CTkFont(size=14, weight="bold"), text_color="#AAAAAA")
        self.tip_title.pack(anchor="w", padx=15, pady=(10, 0))
        self.insight_label = ctk.CTkLabel(self.footer_frame, text="", font=ctk.CTkFont(size=13), wraplength=600, justify="left", text_color="#DDDDDD")
        self.insight_label.pack(anchor="w", padx=15, pady=5)

    def choose_log_file(self):
        path = filedialog.askopenfilename(title="Selecionar Log", filetypes=[("Log files", "*.log"), ("All", "*.*")])
        if path:
            self.log_file_path = path
            self.log_file_label.configure(text=f"Arquivo: {os.path.basename(path)}")
            self.analyze_btn.configure(state="normal")
            self.export_btn.configure(state="normal")

    def analyze_log(self):
        if not self.log_file_path:
            return
        stats = self.log_analyzer.parse_log(self.log_file_path)
        self.log_results_text.delete("0.0", "end")
        text = f"""
Total Linhas: {stats['total_lines']}
Top IPs: {stats['top_ips'][:5]}
Erros: {stats['errors_count']} ({stats['error_rate']:.1f}%)
Sucessos: {stats['success']}
        """
        self.log_results_text.insert("0.0", text)

    def export_log(self):
        if self.log_file_path:
            out_path = self.log_file_path.replace('.log', '_analysis.csv')
            self.log_analyzer.export_csv(self.log_file_path, out_path)
            messagebox.showinfo("Export", f"Exportado para {out_path}")

    def update_stats(self, stats):
        self.app.after(0, self.update_network_tab, stats)

    def update_network_tab(self, stats):
        # Headers
        self.dl_val_label.configure(text=f"{stats['total_dl_mb']:.1f} MB/s")
        self.ul_val_label.configure(text=f"{stats['total_ul_mb']:.1f} MB/s")
        # Insight
        new_tip = self.locales.get(stats['insight'], stats['insight'])
        if new_tip != self.current_tip:
            self.current_tip = new_tip
            self.insight_label.configure(text=new_tip)
        # Apps list & chart
        self.apps_textbox.configure(state="normal")
        self.apps_textbox.delete("1.0", "end")
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        apps = stats['apps']
        if not apps:
            self.apps_textbox.insert("end", self.locales["insight_no_admin"])
            self.pie_chart.update_chart({})
        else:
            sorted_apps = sorted(apps.items(), key=lambda x: (x[1]['dl_kb'] + x[1]['ul_kb']), reverse=True)
            top_apps = {name: data['dl_kb'] + data['ul_kb'] for name, data in sorted_apps[:5] if data['dl_kb'] + data['ul_kb'] > 0}
            self.pie_chart.update_chart(top_apps)
            for i, (app, data) in enumerate(sorted_apps):
                dl_val = f"{data['dl_kb']:.1f}"
                ul_val = f"{data['ul_kb']:.1f}"
                line = f"{app:<25} DL:{dl_val:>6} UL:{ul_val:>6}\n"
                self.apps_textbox.insert("end", line)
                if i < 6:
                    color = self.pie_chart.colors[i % len(self.pie_chart.colors)]
                    l_frame = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
                    l_frame.pack(fill="x", pady=2)
                    ctk.CTkFrame(l_frame, width=12, height=12, fg_color=color).pack(side="left", padx=5)
                    ctk.CTkLabel(l_frame, text=app, font=ctk.CTkFont(size=12)).pack(side="left")
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
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem(self.locales["dashboard"], self.show_window, default=True),
            pystray.MenuItem(self.locales["language"], pystray.Menu(
                pystray.MenuItem("English", self.set_language_en),
                pystray.MenuItem("Português", self.set_language_pt)
            )),
            pystray.MenuItem(self.locales["exit"], self.quit_window)
        )
        self.tray_icon = pystray.Icon("Fuinha", image, self.locales["title"], menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def withdraw_window(self):
        self.app.withdraw()

    def show_window(self, icon=None, item=None):
        self.app.deiconify()

    def quit_window(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.engine.stop()
        self.app.quit()

    def run(self):
        self.engine.start()
        self.init_tray()
        self.app.mainloop()
