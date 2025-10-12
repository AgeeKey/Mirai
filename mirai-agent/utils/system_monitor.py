import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1):
        self.interval = interval

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_memory_info(self):
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percentage': memory.percent
        }

    def get_disk_info(self):
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percentage': disk.percent
        }

    def monitor(self, duration=10):
        end_time = time.time() + duration
        while time.time() < end_time:
            print(f'CPU Usage: {self.get_cpu_usage()}%')
            memory_info = self.get_memory_info()
            print(f'Memory Info: {memory_info}')
            disk_info = self.get_disk_info()
            print(f'Disk Info: {disk_info}')
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=1)
    monitor.monitor(duration=10)