import psutil
import time
import threading

class NetworkMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.thread = None
        self.last_io = psutil.net_io_counters()
        self.app_io = {}
        self.process_totals = {} # New: Tracks total bytes per process

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        while self.running:
            time.sleep(1)
            # System wide network stats
            try:
                current_io = psutil.net_io_counters()
                dl_speed = current_io.bytes_recv - self.last_io.bytes_recv
                ul_speed = current_io.bytes_sent - self.last_io.bytes_sent
                self.last_io = current_io
            except Exception:
                dl_speed, ul_speed = 0, 0
            
            # Active connections per app
            apps = self._get_active_apps()
            
            # Calculate total weighting for speed distribution
            total_conns = sum(apps.values()) if apps else 0
            
            # Distribute total speeds among apps
            processed_apps = {}
            if apps:
                for name, conns in apps.items():
                    weight = conns / total_conns if total_conns > 0 else 0
                    processed_apps[name] = {
                        'conns': conns,
                        'dl_kb': (dl_speed * weight) / 1024,
                        'ul_kb': (ul_speed * weight) / 1024
                    }
            elif dl_speed > 100 or ul_speed > 100:
                # If we have traffic but no apps identification (likely permission issue), attribute to System
                processed_apps["system_others"] = {
                    'conns': 1,
                    'dl_kb': dl_speed / 1024,
                    'ul_kb': ul_speed / 1024
                }

            # Prepare stats for UI
            stats = {
                'total_dl_mb': dl_speed / (1024 * 1024),
                'total_ul_mb': ul_speed / (1024 * 1024),
                'total_dl_kb': dl_speed / 1024,
                'total_ul_kb': ul_speed / 1024,
                'apps': processed_apps,
                'insight': self._generate_insight(dl_speed, ul_speed, apps)
            }
            if self.callback:
                self.callback(stats)

    def _generate_insight(self, dl, ul, apps):
        # Convert to KB/s for easier logic
        dl_kb = dl / 1024
        ul_kb = ul / 1024
        
        if ul_kb > 500 and ul_kb > dl_kb:
            return "insight_upload_saturation"
        if dl_kb > 2000:
            return "insight_high_download"
        if not apps and dl_kb > 50:
            return "insight_no_admin"
        
        # Default/Random tips
        tips = ["insight_tip_1", "insight_tip_2", "insight_tip_3"]
        import random
        return random.choice(tips)

    def _get_active_apps(self):
        apps_found = {}
        try:
            # Try to get all connections. On Linux, this requires root/sudo for PID mapping.
            conns = psutil.net_connections(kind='inet')
            for conn in conns:
                # Filter for ESTABLISHED to focus on active transfers
                if conn.status == 'ESTABLISHED' and conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        name = proc.name()
                        # Some process names on Linux can be obscure, could add a mapper here
                        apps_found[name] = apps_found.get(name, 0) + 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
        except (psutil.AccessDenied, PermissionError):
            # If access denied, apps_found stays empty, trigger the "No Admin" insight
            pass
            
        return apps_found
