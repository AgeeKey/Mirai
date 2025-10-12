import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1, runtime=10):
        self.interval = interval
        self.runtime = runtime

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/').percent
        return disk

    def monitor(self):
        start_time = time.time()
        while (time.time() - start_time) < self.runtime:
            cpu = self.get_cpu_usage()
            memory = self.get_memory_usage()
            disk = self.get_disk_usage()

            print(f'CPU Usage: {cpu}%')
            print(f'Memory Usage: {memory}%')
            print(f'Disk Usage: {disk}%')

            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=1, runtime=10)
    monitor.monitor()