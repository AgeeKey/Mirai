import psutil
import time

def monitor_system(interval=1):
    try:
        while True:
            # Получение данных
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')[0]

            # Вывод данных
            print(f'CPU Usage: {cpu_usage}%')
            print(f'RAM Usage: {ram_info.percent}% ({ram_info.used / (1024 ** 2)} MB / {ram_info.total / (1024 ** 2)} MB)')
            print(f'Disk Usage: {disk_info}%')
            print('-' * 30)
            time.sleep(interval)
    except KeyboardInterrupt:
        print('Monitoring stopped.')

if __name__ == '__main__':
    monitor_system()