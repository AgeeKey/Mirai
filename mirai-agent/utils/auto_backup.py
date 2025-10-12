import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='backup.log', format='%(asctime)s - %(levelname)s - %(message)s')

def backup_files(source_dirs, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создана директория для бэкапа: {backup_dir}')

    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            dest_dir = os.path.join(backup_dir, os.path.basename(source_dir) + '_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
            shutil.copytree(source_dir, dest_dir)
            logging.info(f'Бэкап из {source_dir} был создан в {dest_dir}')
        else:
            logging.warning(f'Исходная директория не найдена: {source_dir}')

if __name__ == '__main__':
    # Замените на пути к вашим важным файлам
    source_directories = ['/path/to/important_file_1', '/path/to/important_file_2']
    backup_directory = '/path/to/backup_directory'
    backup_files(source_directories, backup_directory)
