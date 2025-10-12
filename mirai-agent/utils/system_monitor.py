import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1):
        self.interval = interval

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def run(self):
        while True:
            cpu = self.get_cpu_usage()
            memory = self.get_memory_usage()
            disk = self.get_disk_usage()
            print(f'CPU Usage: {cpu}%, Memory Usage: {memory}%, Disk Usage: {disk}%')
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.run()
