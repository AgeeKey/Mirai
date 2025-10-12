import psutil
import time

def monitor_system(interval=1):
    try:
        while True:
            # Получение информации о CPU
            cpu_usage = psutil.cpu_percent()
            
            # Получение информации о RAM
            memory = psutil.virtual_memory()
            ram_usage = memory.percent
            
            # Получение информации о диске
            disk = psutil.disk_usage('/')[0]
            disk_usage = disk / (1024 ** 3)  # преобразование в ГБ
            
            # Вывод информации
            print(f'CPU Usage: {cpu_usage}%')
            print(f'RAM Usage: {ram_usage}%')
            print(f'Disk Usage: {disk_usage:.2f} GB')
            print('-' * 30)
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print('Monitoring stopped.')

if __name__ == '__main__':
    monitor_system()