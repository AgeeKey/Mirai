import json
import psutil
from datetime import datetime

class Monitoring:
    def __init__(self, metrics_file='metrics.json'):
        self.metrics_file = metrics_file
        self.metrics = {
            'task_count': 0,
            'execution_time': [],
            'error_count': 0,
            'resource_usage': []
        }
        self.load_metrics()

    def load_metrics(self):
        try:
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
        except FileNotFoundError:
            pass

    def save_metrics(self):
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=4)

    def task_completed(self, execution_time):
        self.metrics['task_count'] += 1
        self.metrics['execution_time'].append(execution_time)
        self.save_metrics()

    def task_failed(self):
        self.metrics['error_count'] += 1
        self.save_metrics()

    def record_resource_usage(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        timestamp = datetime.now().isoformat()
        self.metrics['resource_usage'].append({
            'timestamp': timestamp,
            'cpu': cpu_usage,
            'ram': ram_usage
        })
        self.save_metrics()

    def get_health_status(self):
        health_status = {
            'total_tasks': self.metrics['task_count'],
            'total_errors': self.metrics['error_count'],
            'cpu_usage': psutil.cpu_percent(),
            'ram_usage': psutil.virtual_memory().percent
        }
        return health_status

# Example usage:
# monitor = Monitoring()
# monitor.task_completed(0.5)  # example time in seconds
# monitor.task_failed()
# monitor.record_resource_usage()
# print(monitor.get_health_status())
