import psutil
import time

def monitor_system(interval=1):
    try:
        while True:
            # Получение текущей информации о системе
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            
            # Вывод информации
            print(f'CPU Usage: {cpu_usage}%')
            print(f'RAM Usage: {ram_usage}%')
            print(f'Disk Usage: {disk_usage}%')
            print('-' * 30)
            
            # Задержка между проверками
            time.sleep(interval)
    except KeyboardInterrupt:
        print('Monitoring stopped.')

if __name__ == '__main__':
    monitor_system()