import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_backup(source_dirs, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f'Создана директория бэкапа: {backup_dir}')

    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            dest_dir = os.path.join(backup_dir, os.path.basename(source_dir) + '_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
            shutil.copytree(source_dir, dest_dir)
            logging.info(f'Бэкап выполнен: {source_dir} -> {dest_dir}')
        else:
            logging.warning(f'Источник не найден: {source_dir}')

if __name__ == '__main__':
    important_files = ['/path/to/important/files', '/another/path/to/backup']
    backup_location = '/path/to/backup/directory'
    create_backup(important_files, backup_location)