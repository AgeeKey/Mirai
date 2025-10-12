import psutil
import time

class SystemMonitor:
    def __init__(self, interval=1):
        self.interval = interval

    def monitor(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=self.interval)
            ram_usage = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')[3]  # 3 is the free space, 0 is total

            print(f'CPU Usage: {cpu_usage}%')
            print(f'RAM Usage: {ram_usage.percent}%')
            print(f'Disk Free Space: {disk_usage}')
            time.sleep(self.interval)

if __name__ == '__main__':
    monitor = SystemMonitor()  # 1-second interval
    monitor.monitor()