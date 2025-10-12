import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создан каталог для бэкапа: {backup_dir}')

    # Перебор всех файлов в исходной директории
    try:
        for filename in os.listdir(source_dir):
            full_file_name = os.path.join(source_dir, filename)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, backup_dir)
                logging.info(f'Файл {full_file_name} успешно скопирован в {backup_dir}')
    except Exception as e:
        logging.error(f'Ошибка при бэкапе: {e}')

if __name__ == '__main__':
    # Задаем директории
    source_directory = 'path/to/important/files'
    backup_directory = 'path/to/backup/directory'
    backup_files(source_directory, backup_directory)
