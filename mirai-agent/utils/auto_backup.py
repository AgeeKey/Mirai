import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к важным файлам и месту назначения бэкапа
important_files = ['/path/to/important/file1', '/path/to/important/file2']  # Укажите важные файлы
backup_destination = '/path/to/backup/directory/'  # Укажите директорию для бэкапа

def create_backup():
    try:
        os.makedirs(backup_destination, exist_ok=True)
        for file in important_files:
            if os.path.isfile(file):
                shutil.copy(file, backup_destination)
                logging.info(f'Бэкап {file} создан успешно.')
            else:
                logging.warning(f'Файл не найден: {file}')
    except Exception as e:
        logging.error(f'Ошибка при создании бэкапа: {e}')

if __name__ == '__main__':
    create_backup()
