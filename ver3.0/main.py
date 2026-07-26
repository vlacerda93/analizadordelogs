import sys
import os
from utils import is_admin, run_as_admin
from monitor_engine import NetworkMonitor
from ui_manager import UIManager

def main():
    if not is_admin() and os.name == 'nt':
        if "--no-admin" not in sys.argv:
            print("Requisitando permissões de Administrador...")
            try:
                run_as_admin()
                return
            except Exception as e:
                print(f"Não foi possível elevar privilégios: {e}. Executando em modo usuário...")

    engine = NetworkMonitor(callback=None)
    ui = UIManager(engine)
    ui.run()

if __name__ == "__main__":
    main()
