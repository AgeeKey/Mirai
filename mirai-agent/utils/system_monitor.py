import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1):
        self.interval = interval

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def monitor(self):
        while True:
            cpu_usage = self.get_cpu_usage()
            memory_usage = self.get_memory_usage()
            disk_usage = self.get_disk_usage()
            print(f'CPU Usage: {cpu_usage}%')
            print(f'Memory Usage: {memory_usage}%')
            print(f'Disk Usage: {disk_usage}%')
            time.sleep(self.interval)