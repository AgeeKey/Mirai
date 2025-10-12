import psutil
import time


def display_system_info():
    # Получение информации о CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")
    
    # Получение информации о RAM
    ram = psutil.virtual_memory()
    print(f"RAM Usage: {ram.percent}% ({ram.used / (1024 ** 3):.2f} GB используемой из {ram.total / (1024 ** 3):.2f} GB)")
    
    # Получение информации о диске
    disk = psutil.disk_usage('/')
    print(f"Disk Usage: {disk.percent}% ({disk.used / (1024 ** 3):.2f} GB используемой из {disk.total / (1024 ** 3):.2f} GB)")


if __name__ == '__main__':
    while True:
        display_system_info()
        time.sleep(5)  # Обновление каждые 5 секунд
