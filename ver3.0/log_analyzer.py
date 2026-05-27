import re
import os
from collections import Counter
from datetime import datetime
import csv
import psutil

class LogAnalyzer:
    def __init__(self):
        self.log_patterns = {
            'ip': r'^(\S+) ',  # IP first field
            'status': r'\".*? (\d{3}) ',  # Status code
            'error': r'(error|failed|401|500|403)',
            'timestamp': r'\[(.*?)\]'
        }

    def parse_log(self, log_path):
        """Parse access.log like Apache format. Returns dict with stats."""
        if not os.path.exists(log_path):
            return {'error': 'Arquivo não encontrado'}

        stats = {
            'total_lines': 0,
            'top_ips': Counter(),
            'errors': [],
            'success': 0,
            'errors_count': 0,
            'raw_lines': []
        }

        with open(log_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stats['total_lines'] += 1
                stats['raw_lines'].append((line_num, line.strip()))

                # IP
                ip_match = re.match(self.log_patterns['ip'], line)
                if ip_match:
                    stats['top_ips'][ip_match.group(1)] += 1

                # Status
                if ' 200 ' in line:
                    stats['success'] += 1
                status_match = re.search(r'\".*? (\d{3}) ', line)
                if status_match and int(status_match.group(1)) >= 400:
                    stats['errors'].append(line.strip())

                # Keyword errors
                if re.search(self.log_patterns['error'], line, re.I):
                    stats['errors_count'] += 1

        stats['top_ips'] = stats['top_ips'].most_common(10)
        stats['error_rate'] = (stats['errors_count'] / stats['total_lines'] * 100) if stats['total_lines'] else 0

        return stats

    def filter_logs(self, log_path, filter_type='all', keyword=None):
        """Filter lines by type or keyword."""
        stats = self.parse_log(log_path)
        filtered = []
        for line_num, line in stats['raw_lines']:
            if filter_type == 'errors' or (keyword and keyword.lower() in line.lower()):
                filtered.append(f"L{line_num}: {line}")
        return filtered

    def export_csv(self, log_path, output_path):
        """Export top_ips to CSV."""
        stats = self.parse_log(log_path)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['IP', 'Count'])
            writer.writerows(stats['top_ips'])
        return True

    def check_auth_logs(self):
        log_paths = ['/var/log/auth.log', '/var/log/secure']
        failed_attempts = 0
        details = []
        for path in log_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line in lines[-1000:]:
                            if 'Failed password' in line or 'authentication failure' in line or 'invalid user' in line.lower():
                                failed_attempts += 1
                                details.append(line.strip())
                    break # Se leu com sucesso, para
                except PermissionError:
                    return f"Erro: Permissão negada. Execute o Fuinha como root/sudo para ler {path}."
                except Exception as e:
                    return f"Erro ao ler {path}: {str(e)}"
                
        if not details and failed_attempts == 0:
            return "✅ Nenhuma tentativa de intrusão detectada nos logs de sistema recentes."
            
        res = f"⚠️ ATENÇÃO: {failed_attempts} tentativas de intrusão (falhas de login) detectadas recentemente!\n\nÚltimos registros suspeitos:\n"
        for d in details[-15:]:
            res += f"- {d}\n"
        return res

    def check_open_ports(self):
        res = "🔍 Auditoria de Portas Abertas (Servidores locais aguardando conexão):\n\n"
        res += f"{'PROCESSO':<25} {'PORTA':<10} {'STATUS':<15}\n"
        res += "-"*50 + "\n"
        try:
            conns = psutil.net_connections(kind='inet')
            listening = [c for c in conns if c.status == 'LISTEN']
            if not listening:
                return res + "Nenhuma porta aberta detectada."
                
            for c in listening:
                try:
                    proc = psutil.Process(c.pid) if c.pid else None
                    name = proc.name() if proc else "Sistema/Desconhecido"
                except:
                    name = "Restrito"
                port = c.laddr.port if c.laddr else "N/A"
                res += f"{name:<25} {port:<10} {c.status:<15}\n"
        except (psutil.AccessDenied, PermissionError):
            return "Erro: Permissão negada para listar conexões. Execute como sudo."
            
        return res

# Example usage
if __name__ == '__main__':
    analyzer = LogAnalyzer()
    print(analyzer.parse_log('../ver1.0/access.log'))
