import psutil
import time

def monitor_system(interval=1):
    print("Monitoring system resources...\n")
    while True:
        cpu_usage = psutil.cpu_percent(interval=interval)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/').percent
        print(f"CPU Usage: {cpu_usage}%")
        print(f"RAM Usage: {memory_info.percent}% (Used: {memory_info.used / (1024**2):.2f} MB, Total: {memory_info.total / (1024**2):.2f} MB)")
        print(f"Disk Usage: {disk_usage}%\n")
        time.sleep(interval)

if __name__ == '__main__':
    monitor_system()