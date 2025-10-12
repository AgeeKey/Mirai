import psutil
import time

def monitor_system(interval=1):
    while True:
        # Получаем загрузку CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        # Получаем использование RAM
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        # Получаем использование диска
        disk = psutil.disk_usage('/')