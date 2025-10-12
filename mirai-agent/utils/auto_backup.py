import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к важным файлам и директории бэкапа
important_files = ['/path/to/important/file1', '/path/to/important/file2']  # Замените на ваши файлы
backup_directory = '/path/to/backup/directory/'  # Замените на путь к директории бэкапа

def create_backup():
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
        logging.info(f'Создана директория резервного копирования: {backup_directory}')

    for file in important_files:
        try:
            shutil.copy(file, backup_directory)
            logging.info(f'Файл {file} успешно скопирован в {backup_directory}')
        except Exception as e:
            logging.error(f'Ошибка при копировании файла {file}: {e}')  

if __name__ == '__main__':
    create_backup()
