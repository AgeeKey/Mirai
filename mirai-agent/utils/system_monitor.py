import psutil

class SystemMonitor:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

if __name__ == '__main__':
    monitor = SystemMonitor()
    cpu = monitor.get_cpu_usage()
    memory = monitor.get_memory_usage()
    disk = monitor.get_disk_usage()
    print(f'CPU Usage: {cpu}%')
    print(f'Memory Usage: {memory}%')
    print(f'Disk Usage: {disk}%')