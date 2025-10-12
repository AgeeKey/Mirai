import psutil

class SystemMonitor:
    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def monitor(self):
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()
        print(f"CPU Usage: {cpu}% | Memory Usage: {memory}% | Disk Usage: {disk}%")

if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.monitor()