import psutil
import time

# Функция для мониторинга системы

def monitor_system(duration=10, interval=1):
    end_time = time.time() + duration
    while time.time() < end_time:
        # Получаем данные о загрузке CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        # Получаем данные о загрузке RAM
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        # Получаем данные о загрузке диска
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        
        # Выводим данные
        print(f"CPU Usage: {cpu_usage}%")
        print(f"RAM Usage: {ram_usage}%")
        print(f"Disk Usage: {disk_usage}%")
        print("---")
        time.sleep(interval)

if __name__ == '__main__':
    monitor_system(duration=10)  # Изменение: ограничить время мониторинга до 10 секунд