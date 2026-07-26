import sys
import os
import ctypes

def get_asset_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def is_admin():
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except:
        return False

def run_as_admin():
    if os.name == 'nt':
        import ctypes
        script_path = os.path.abspath(sys.argv[0])
        script_dir = os.path.dirname(script_path)
        args = f'"{script_path}" ' + " ".join(sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, script_dir, 1)
        sys.exit()
    else:
        # On linux, just print or let it run without some process permissions
        pass
