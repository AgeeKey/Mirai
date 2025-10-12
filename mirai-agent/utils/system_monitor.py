import psutil
import time

def monitor_system(interval=1):
    try:
        while True:
            # Получение информации о CPU
            cpu_usage = psutil.cpu_percent(interval=interval)
            # Получение информации о RAM
            ram = psutil.virtual_memory()
            ram_usage = ram.percent
            # Получение информации о диске
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # Вывод информации
            print(f'CPU Usage: {cpu_usage}%')
            print(f'RAM Usage: {ram_usage}%')
            print(f'Disk Usage: {disk_usage}%')
            print('-' * 30)
            
    except KeyboardInterrupt:
        print('Monitoring stopped.')

if __name__ == '__main__':
    monitor_system()