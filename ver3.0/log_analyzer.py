import re
import os
from collections import Counter
from datetime import datetime
import csv

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

# Example usage
if __name__ == '__main__':
    analyzer = LogAnalyzer()
    print(analyzer.parse_log('../ver1.0/access.log'))
