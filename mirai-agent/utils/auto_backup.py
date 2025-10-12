import os
import shutil
import logging
import time
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к важным файлам и директории бэкапа
important_files = ['/path/to/your/important_file1', '/path/to/your/important_file2']
backup_directory = '/path/to/your/backup_directory'

# Функция для создания бэкапа
def create_backup():
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
        logging.info(f'Создана директория бэкапа: {backup_directory}')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(backup_directory, f'backup_{timestamp}')
    os.makedirs(backup_folder)
    logging.info(f'Создана новая папка бэкапа: {backup_folder}')

    for file in important_files:
        if os.path.exists(file):
            shutil.copy(file, backup_folder)
            logging.info(f'Файл {file} скопирован в {backup_folder}')
        else:
            logging.warning(f'Файл не найден: {file}')

if __name__ == '__main__':
    create_backup()
    logging.info('Бэкап завершен.')