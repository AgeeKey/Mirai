import psutil
import time

class SystemMonitor:
    def __init__(self):
        pass

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return ram.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')[0]
        return disk

    def monitor(self):
        while True:
            cpu = self.get_cpu_usage()
            ram = self.get_ram_usage()
            disk = self.get_disk_usage()
            print(f'CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%')
            time.sleep(1)  # Pause for 1 second

if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.monitor()