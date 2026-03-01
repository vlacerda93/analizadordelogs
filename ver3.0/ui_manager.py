import customtkinter as ctk
import tkinter as tk
import pystray
from PIL import Image, ImageDraw
import threading
import json
import locale
import sys
import os
from utils import get_asset_path

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
        start_ang = 0
        
        # Center and Radius
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
        self.app.title("Fuinha - Network Monitor")
        self.app.geometry("450x600")
        
        # UI Elements Initialization
        self.header_frame = None
        self.dl_block = None
        self.dl_val_label = None
        self.ul_block = None
        self.ul_val_label = None
        self.table_frame = None
        self.labels_frame = None
        self.apps_textbox = None
        self.footer_frame = None
        self.tip_title = None
        self.insight_label = None
        self.tray_icon = None
        self.locales = {}
        self.pie_chart = None # New attribute
        
        ctk.set_appearance_mode("dark")
        
        self.language = "en"
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
        except Exception as e:
            self.locales = {
                "title": "Fuinha Network Monitor",
                "dashboard": "Show Dashboard",
                "language": "Language",
                "exit": "Exit",
                "upload": "Upload",
                "download": "Download",
                "active_apps": "Active Apps Connections",
                "insight": f"Insight: Error loading language ({e})"
            }

    def setup_ui(self):
        # Clear existing widgets if re-running
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.title(self.locales["title"])
        self.app.geometry("550x700") # Slightly wider for the new layout
        
        # --- Speed Headers (Gradients/Large Blocks) ---
        self.header_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=20)

        # Download Block
        self.dl_block = ctk.CTkFrame(self.header_frame, fg_color="#1a1a1a", border_width=2, border_color="#00FFAA")
        self.dl_block.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(self.dl_block, text=self.locales["download"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#00FFAA").pack(pady=(10, 0))
        self.dl_val_label = ctk.CTkLabel(self.dl_block, text="0.0 MB/s", font=ctk.CTkFont(size=28, weight="bold"))
        self.dl_val_label.pack(pady=(0, 10))

        # Upload Block
        self.ul_block = ctk.CTkFrame(self.header_frame, fg_color="#1a1a1a", border_width=2, border_color="#FF8800")
        self.ul_block.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(self.ul_block, text=self.locales["upload"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#FF8800").pack(pady=(10, 0))
        self.ul_val_label = ctk.CTkLabel(self.ul_block, text="0.0 MB/s", font=ctk.CTkFont(size=28, weight="bold"))
        self.ul_val_label.pack(pady=(0, 10))

        # --- Process Table Header ---
        self.table_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=20)

        self.apps_label = ctk.CTkLabel(self.table_frame, text=self.locales["active_apps"], font=ctk.CTkFont(size=16, weight="bold"))
        self.apps_label.pack(anchor="w", pady=(10, 5))

        # --- Pie Chart Container ---
        self.chart_container = ctk.CTkFrame(self.table_frame, fg_color="#1a1a1a", height=200)
        self.chart_container.pack(fill="x", pady=10)
        self.chart_container.pack_propagate(False)
        
        self.pie_chart = PieChart(self.chart_container, bg="#1a1a1a", width=180, height=180)
        self.pie_chart.pack(side="left", padx=20)
        
        self.legend_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.legend_frame.pack(side="left", fill="both", expand=True, pady=10)
        
        # --- Process Table Header ---
        # (Table headers and textbox follow)

        # Scrolled Text for list
        self.apps_textbox = ctk.CTkTextbox(self.table_frame, font=ctk.CTkFont(family="Consolas", size=13))
        self.apps_textbox.pack(fill="both", expand=True, pady=5)
        self.apps_textbox.configure(state="disabled")

        # --- Fuinha Tip Box (Footer) ---
        self.footer_frame = ctk.CTkFrame(self.app, fg_color="#1a1a1a", height=100)
        self.footer_frame.pack(fill="x", padx=20, pady=20)
        self.footer_frame.pack_propagate(False)

        self.tip_title = ctk.CTkLabel(self.footer_frame, text=f"✨ {self.locales['fuinha_tip_title']}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#AAAAAA")
        self.tip_title.pack(anchor="w", padx=15, pady=(10, 0))

        self.insight_label = ctk.CTkLabel(
            self.footer_frame, 
            text="", 
            font=ctk.CTkFont(size=13, slant="italic"), 
            wraplength=480,
            justify="left",
            text_color="#DDDDDD"
        )
        self.insight_label.pack(anchor="w", padx=15, pady=5)

    def update_stats(self, stats):
        self.app.after(0, self._update_ui_elements, stats)

    def _update_ui_elements(self, stats):
        # Update Main Counters
        self.dl_val_label.configure(text=f"{stats['total_dl_mb']:.1f} MB/s")
        self.ul_val_label.configure(text=f"{stats['total_ul_mb']:.1f} MB/s")
        
        # Update Insight
        insight_msg = self.locales.get(stats['insight'], stats['insight'])
        self.insight_label.configure(text=insight_msg)
        
        # Update Process List & Legend
        self.apps_textbox.configure(state="normal")
        self.apps_textbox.delete("1.0", "end")
        
        for widget in self.legend_frame.winfo_children():
            widget.destroy()

        apps = stats['apps']
        if not apps:
            self.apps_textbox.insert("end", f"\n   {self.locales['insight_no_admin']}\n")
            self.pie_chart.update_chart({})
        else:
            # Sort apps by current total activity (dl + ul)
            # x[1] is a dict like {'dl_kb': 5.0, 'ul_kb': 0.5, 'conns': 2}
            sorted_apps = sorted(apps.items(), key=lambda x: x[1]['dl_kb'] + x[1]['ul_kb'], reverse=True)
            
            # top_apps for chart: map process name to total KB/s
            top_apps = {name: data['dl_kb'] + data['ul_kb'] for name, data in sorted_apps[:5]}
            if len(sorted_apps) > 5:
                # Sum the rest into "Other"
                other_sum = sum(data['dl_kb'] + data['ul_kb'] for name, data in sorted_apps[5:])
                if other_sum > 0:
                    top_apps["Other"] = other_sum

            self.pie_chart.update_chart(top_apps)

            for i, (app, data) in enumerate(sorted_apps):
                color = self.pie_chart.colors[i % len(self.pie_chart.colors)] if i < 6 else "gray"
                
                # Update Table
                # Format: [Name] [DL KB/s] [UL KB/s]
                dl_val = f"{data['dl_kb']:.1f}" if data['dl_kb'] > 0 else "0.0"
                ul_val = f"{data['ul_kb']:.1f}" if data['ul_kb'] > 0 else "0.0"
                
                line = f" {app:<25} {dl_val:>10} {ul_val:>10}\n"
                self.apps_textbox.insert("end", line)
                
                # Update Legend (only for top processes)
                if i < 6:
                    l_frame = ctk.CTkFrame(self.legend_frame, fg_color="transparent")
                    l_frame.pack(fill="x", pady=2)
                    ctk.CTkFrame(l_frame, width=12, height=12, fg_color=color).pack(side="left", padx=5)
                    ctk.CTkLabel(l_frame, text=f"{app}", font=ctk.CTkFont(size=12)).pack(side="left")

        self.apps_textbox.configure(state="disabled")

    def create_image(self):
        # Try to load from assets first
        path = get_asset_path('assets/icon.png')
        try:
            if os.path.exists(path):
                return Image.open(path)
        except Exception:
            pass

        # Fallback: Generate a green square icon with an 'F' inside
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, 64, 64), radius=16, fill=(0, 200, 100))
        draw.text((22, 10), "F", fill="white", font=None, align="center")
        return image

    def set_language_en(self, icon, item):
        self.language = "en"
        self._apply_locale()
        self.app.after(0, self.setup_ui) 

    def set_language_pt(self, icon, item):
        self.language = "pt_BR"
        self._apply_locale()
        self.app.after(0, self.setup_ui) 

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
        self.tray_icon = pystray.Icon("Fuinha", image, "Fuinha", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def withdraw_window(self):
        self.app.withdraw()

    def show_window(self, icon=None, item=None):
        self.app.after(0, self.app.deiconify)

    def quit_window(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.engine.stop()
        self.app.after(0, self.app.quit)

    def run(self):
        self.engine.start()
        self.init_tray()
        self.app.mainloop()
