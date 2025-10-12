import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1):
        self.interval = interval

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return ram.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/');
        return disk.percent

    def monitor(self):
        while True:
            cpu = self.get_cpu_usage()
            ram = self.get_ram_usage()
            disk = self.get_disk_usage()
            print(f'CPU Usage: {cpu}% | RAM Usage: {ram}% | Disk Usage: {disk}%')
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=1)
    monitor.monitor()