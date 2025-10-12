import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1, duration=10):
        self.interval = interval
        self.duration = duration

    def get_system_stats(self):
        cpu_usage = psutil.cpu_percent()  # CPU usage percentage
        ram_usage = psutil.virtual_memory().percent  # RAM usage percentage
        disk_usage = psutil.disk_usage('/').percent  # Disk usage percentage
        return cpu_usage, ram_usage, disk_usage

    def run(self):
        for _ in range(self.duration):
            cpu, ram, disk = self.get_system_stats()
            print(f'CPU Usage: {cpu}%, RAM Usage: {ram}%, Disk Usage: {disk}%')
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor(interval=1, duration=10)
    monitor.run()