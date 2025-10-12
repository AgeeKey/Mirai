import os
import shutil
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    filename='backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def backup_files(source_dir, backup_dir):
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Created backup directory: {backup_dir}')

        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            backup_file = os.path.join(backup_dir, filename)
            if os.path.isfile(source_file):
                shutil.copy2(source_file, backup_file)
                logging.info(f'Copied: {source_file} to {backup_file}')  

        logging.info('Backup completed successfully.')
    except Exception as e:
        logging.error(f'Error during backup: {e}')

if __name__ == '__main__':
    source_directory = 'path/to/important/files'  # Измените на реальный путь
    backup_directory = 'path/to/backup'  # Измените на реальный путь
    backup_files(source_directory, backup_directory)