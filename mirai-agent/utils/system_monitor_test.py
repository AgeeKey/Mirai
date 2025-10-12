import psutil

class SystemMonitor:
    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/').percent
        return disk

if __name__ == '__main__':
    monitor = SystemMonitor()
    print(f"CPU Usage: {monitor.get_cpu_usage()}% | Memory Usage: {monitor.get_memory_usage()}% | Disk Usage: {monitor.get_disk_usage()}%")