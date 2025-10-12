import psutil
import time

def monitor_system():
    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            print(f"CPU Usage: {cpu_usage}%")
            print(f"RAM Usage: {ram_usage}%")
            print(f"Disk Usage: {disk_usage}%")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == '__main__':
    monitor_system()