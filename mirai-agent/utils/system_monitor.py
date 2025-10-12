import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1, duration=10):  # добавим параметр длительности
        self.interval = interval
        self.duration = duration

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=self.interval)

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return ram.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def monitor(self):
        start_time = time.time()
        while (time.time() - start_time) < self.duration:
            cpu_usage = self.get_cpu_usage()
            ram_usage = self.get_ram_usage()
            disk_usage = self.get_disk_usage()
            print(f"CPU Usage: {cpu_usage}% | RAM Usage: {ram_usage}% | Disk Usage: {disk_usage}%")
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=1, duration=10)
    monitor.monitor()