import sys
import os
from utils import is_admin, run_as_admin
from monitor_engine import NetworkMonitor
from ui_manager import UIManager

def main():
    if not is_admin() and os.name == 'nt':
        # Prompt UAC if not admin on Windows
        print("Requisitando permissões de Administrador...")
        run_as_admin()
        return

    engine = NetworkMonitor(callback=None)
    ui = UIManager(engine)
    ui.run()

if __name__ == "__main__":
    main()
